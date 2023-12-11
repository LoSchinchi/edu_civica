const EMAIL = document.getElementById('email-inp');
const PASSWORD = document.getElementById('passwd-inp');
const BTN_LOGIN = document.getElementById('btn-login');

const setBtnDisabled = () => BTN_LOGIN.disabled = !EMAIL.value.trim() || !PASSWORD.value.trim();

EMAIL.addEventListener('keyup', setBtnDisabled);
PASSWORD.addEventListener('keyup', setBtnDisabled);

setBtnDisabled();
