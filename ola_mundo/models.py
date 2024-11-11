# Estrutura do banco de dados
from email.policy import default
from enum import unique

from sqlalchemy.orm import backref

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
    fotos = database.relationship('Foto', backref='usuario', lazy=True)


class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem =database.Column(database.String, default='default.png')
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

#
# class Projeto(database.Model):
#     id = database.Column(database.Integer, primary_key=True)
#     nome = database.Column(database.String, nullable=False)
#     categoria = database.Column(database.String, nullable=False)
#     descricao = database.Column(database.String, nullable=False)
