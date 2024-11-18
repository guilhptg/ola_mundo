# é o views do django
from crypt import methods
from datetime import datetime
from idlelib.pyshell import idle_showwarning

from flask import render_template, url_for, request, current_app, redirect
from flask_login import current_user
from werkzeug.utils import redirect
from wtforms.validators import email

from ola_mundo import app, bcrypt, database
from ola_mundo.models import Usuario, Foto
from flask_login import login_required, login_user, logout_user
from ola_mundo.forms import FormLogin, FormCriarConta, FormFoto
import os
from werkzeug.utils import secure_filename


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
            print('Logado')
            return redirect(url_for('perfil', id_usuario=usuario.id))
    return render_template('login.html', form=formlogin)


@app.route('/criarconta', methods=['GET', 'POST'])
def criar_conta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)
        usuario = Usuario(
            username=formcriarconta.username.data,
            senha=senha, email=formcriarconta.email.data
        )
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for('perfil', id_usuario=usuario.id))
    return render_template('criarconta.html', form=formcriarconta)


@app.route('/perfil/<id_usuario>', methods=['GET', 'POST'])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        # acessar o própipo perfil
        formfoto = FormFoto()
        if formfoto.validate_on_submit():
            nome = formfoto.nome.data
            categoria = formfoto.categoria.data
            descricao = formfoto.descricao.data
            link_repositorio = formfoto.link_repositorio.data

            arquivo = formfoto.icone.data
            nome_seguro = secure_filename(arquivo.filename)

            # TODO salver o arquivo na pasta fotos posts - OK
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              app.config['UPLOAD_FOLDER'], nome_seguro)
            arquivo.save(caminho)

            # TODO registrar esse arquivo no banco de dados - OK
            foto = Foto(icone=nome_seguro , id_usuario=current_user.id, nome=nome, categoria=categoria, descricao=descricao, link_repositorio=link_repositorio)
            database.session.add(foto)
            database.session.commit()
            print('foto enviada')
        return render_template('perfil.html', usuario=current_user, form=formfoto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario, form=None)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/feed')
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template('feed.html', fotos=fotos)
