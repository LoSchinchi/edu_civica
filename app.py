from flask import Flask, render_template

app = Flask(__name__)


@app.route('/login-aggiornamenti', methods=['GET'])
def login():
    return render_template('login-aggiornamenti.html')


@app.route('/aggiornamenti', methods=['POST'])
def index():
    return render_template('aggiornamenti.html')


app.run(host='0.0.0.0', debug=True)
