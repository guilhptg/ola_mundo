# Estrutura do banco de dados
from email.policy import default
from enum import unique
from tkinter.ttk import Treeview

from sqlalchemy.orm import backref
from wtforms.widgets.core import Input

from ola_mundo import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    fotos = database.relationship('Foto', backref='usuario', lazy=True, cascade="all, delete-orphan")
    contato = database.relationship('Contato', backref='usuario', lazy=True, uselist=False)
    is_superuser = database.Column(database.Boolean, default=False)


class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    icone =database.Column(database.String, default='default.png')
    nome = database.Column(database.String, nullable=False)
    categoria_id = database.Column(database.Integer, database.ForeignKey('categoria.id'), nullable=True)
    descricao = database.Column(database.String(600), nullable=False)
    link_repositorio = database.Column(database.String, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id', ondelete='CASCADE'))
    tags = database.relationship('Tag', secondary='foto_tag', backref=backref('fotos', lazy=True))
    ativo = database.Column(database.Boolean, default=True)


class Contato(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    linkedin = database.Column(database.String, nullable=False)
    github = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'))

# TODO categoria
class Categoria(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(50), nullable=False, unique=True)


# TODO tag
class Tag(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(20), nullable=False, unique=True)


foto_tag = database.Table(
    'foto_tag',
    database.Column('foto_id', database.Integer, database.ForeignKey('foto.id'), primary_key=True),
    database.Column('tag_id', database.Integer, database.ForeignKey('tag.id'), primary_key=True)
)