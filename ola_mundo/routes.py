# é o views do django
from crypt import methods

from flask import render_template, url_for, request
from ola_mundo import app
from flask_login import login_required
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


@app.route('/criarconta')
def criar_conta():
    formcriarconta = FormCriarConta()

    return render_template('criarconta.html', form=formcriarconta)


@app.route('/perfil/<usuario>')
@login_required
def perfil(usuario):
    return render_template('perfil.html', usuario=usuario)


@app.route('/projetos')
def projetos():
    return render_template('projetos.html')