# é o views do django
from crypt import methods
from idlelib.pyshell import idle_showwarning

from flask import render_template, url_for, request, current_app
from sqlalchemy.sql.functions import current_user
from werkzeug.utils import redirect
from wtforms.validators import email

from ola_mundo import app, bcrypt, database
from ola_mundo.models import Usuario, Foto
from flask_login import login_required, login_user, logout_user
from ola_mundo.forms import FormLogin, FormCriarConta, FormProjetos


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):
            login_user(usuario)
            return redirect(url_for('perfil', id_usuario=usuario.id))
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
        return redirect(url_for('perfil', usuario=usuario.username))
    return render_template('criarconta.html', form=formcriarconta)


@app.route('/perfil/<id_usuario>')
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        # acessar o própipo perfil
        return render_template('perfil.html', usuario=current_user)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/projetos')
def projetos():
    formprojetos = FormProjetos()
    if formprojetos.validate_on_submit():
        pass
    return render_template('projetos.html')