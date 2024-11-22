# é o views do django
from crypt import methods
from datetime import datetime
from idlelib.pyshell import idle_showwarning
from multiprocessing.reduction import send_handle

from flask import render_template, url_for, request, current_app, redirect
from flask_login import current_user
from flask.cli import with_appcontext
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash
from wtforms.validators import email

from ola_mundo import app, bcrypt, database
from ola_mundo.models import Usuario, Foto, Contato, Categoria
from flask_login import login_required, login_user, logout_user
from ola_mundo.forms import FormLogin, FormCriarConta, FormFoto, FormContato, FormCategoria
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


@app.route('/criar-conta', methods=['GET', 'POST'])
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
    return render_template('criar_conta.html', form=formcriarconta)


# @app.cli.command("createsuperuser")
# @with_appcontext
# def create_superuser():
#     nome = input("Digite o nome do superusuário: ")
#     email = input("Digite o email do superusuário: ")
#     senha = input("Digite a senha do superusuário: ")
#
#     if not nome or not email or not senha:
#         print("Todos os campos são obrigatórios.")
#         return
#
#     hashed_senha = generate_password_hash(senha, method='sha256')
#
#     # Verificar se o superusuário já existe
#     existing_user = Usuario.query.filter_by(email=email).first()
#     if existing_user:
#         print(f"Já existe um usuário com o email {email}.")
#         return
#
#     superuser = Usuario(nome=nome, email=email, senha=hashed_senha, is_superuser=True)
#     database.session.add(superuser)
#     database.session.commit()
#     print(f"Superusuário {nome} criado com sucesso!")


@app.route('/perfil/<id_usuario>', methods=['GET', 'POST'])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        # acessar o própipo perfil
        formfoto = FormFoto()
        mensagem_formfoto = False
        categorias = Categoria.query.all()
        formfoto.categoria.choices = [(categoria.id, categoria.nome) for categoria in categorias]
        if formfoto.validate_on_submit():
            nome = formfoto.nome.data
            categoria_id = formfoto.categoria.data
            descricao = formfoto.descricao.data
            link_repositorio = formfoto.link_repositorio.data

            arquivo = formfoto.icone.data
            nome_seguro = secure_filename(arquivo.filename)

            # TODO salver o arquivo na pasta fotos posts - OK
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              app.config['UPLOAD_FOLDER'], nome_seguro)
            arquivo.save(caminho)

            # TODO registrar esse arquivo no banco de dados - OK
            foto = Foto(icone=nome_seguro , id_usuario=current_user.id, nome=nome, categoria_id=categoria_id, descricao=descricao, link_repositorio=link_repositorio)
            database.session.add(foto)
            database.session.commit()

            # reset
            formfoto = FormFoto()
            formfoto.categoria.choices = [(categoria.id, categoria.nome) for categoria in categorias]

            mensagem_formfoto = True
            print('Foto enviada com sucesso!')
        return render_template('perfil.html', usuario=current_user, formfoto=formfoto, mensagem_formfoto=mensagem_formfoto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario, formfoto=None, mensagem_formfoto=False)


# TODO função de remover imagem
# TODO função de curtir imagem


# TODO função de administratção
@app.route('/administracao', methods=['GET', 'POST'])
@login_required
def administracao():
    mensagem_formcategoria = False
    formcategoria = FormCategoria()
    categorias = Categoria.query.all()
    if formcategoria.validate_on_submit():
        nome = formcategoria.nome.data
        categoria = Categoria(nome=nome)
        database.session.add(categoria)
        database.session.commit()
        print('Categoria adicionada')
        mensagem_formcategoria = True
    return render_template('administracao.html', usuario=current_user.id, formcategoria=formcategoria, mensagem_formcategoria=mensagem_formcategoria, categorias=categorias)


# TODO confirgurações do perfil
@app.route('/configuracao', methods=['GET', 'POST'])
@login_required
def configuracao_conta():
    formcontato = FormContato()
    if formcontato.validate_on_submit():
        linkedin = formcontato.linkedin.data
        github = formcontato.github.data
        email = formcontato.github.data
        contato = Contato(linkedin=linkedin, github=github, email=email, id_usuario=current_user.id)
        database.session.add(contato)
        database.session.commit()
    return render_template('configuracao.html', usuario=current_user.id, formcontato=formcontato)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    print('deslogado')
    return redirect(url_for('homepage'))


@app.route('/feed')
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template('feed.html', fotos=fotos)
