# é o views do django
from crypt import methods

from flask import render_template, url_for, request
from werkzeug.utils import redirect
from wtforms.validators import email

from ola_mundo import app, bcrypt, database
from ola_mundo.models import Usuario, Foto
from flask_login import login_required, login_user, logout_user
from ola_mundo.forms import FormLogin, FormCriarConta


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    formlogin = FormLogin()
    if request.method == 'POST':
        dados = request.POST.dict()
        print(dados)
    return render_template('login.html', form=formlogin)


@app.route('/criarconta', methods=['GET', 'POST'])
def criar_conta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        usuario = Usuario(
            username=formcriarconta.username.data,
            senha=senha,
            email=formcriarconta.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect('perfil', usuario=usuario.username)

    return render_template('criarconta.html', form=formcriarconta)


@app.route('/perfil/<usuario>')
@login_required
def perfil(usuario):
    return render_template('perfil.html', usuario=usuario)


@app.route('/projetos')
def projetos():
    return render_template('projetos.html')