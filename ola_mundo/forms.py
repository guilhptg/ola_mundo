# Formuários
from datetime import datetime
from email.policy import default
from wsgiref.validate import validator

from email_validator import validate_email
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.fields.simple import URLField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, length

from ola_mundo import database
from ola_mundo.models import Usuario

# Adicionar RECAPTCHA
class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    botao_confirmacao = SubmitField('Fazer login')


class FormCriarConta(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()], description='Digite seu e-mail')
    username = StringField('Nome do Usuário', validators=[DataRequired(), Length(6, 60)], description='Digite um nome para seu Username')
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)], description='Digite uma senha segura.')
    confirmacao_senha = PasswordField('Confirmação de Senha', validators=[DataRequired(), EqualTo('senha')], description='Repita a mesma senha')
    botao_confirmacao = SubmitField('Criar conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            return ValidationError('E-mail ja cadastrado, faça login para continuar')


class FormFoto(FlaskForm):
    icone = FileField('Icone', validators=[FileRequired()], description='Escolha uma imagem para ser o Icone.')
    nome = StringField('Nome', validators=[DataRequired()])
    categoria = StringField('Categoria', validators=[DataRequired()], description='Digite o segmento ou categoria')
    descricao = StringField('Descrição', validators=[DataRequired(), Length(1,400)], description='Diga em até 400 palavras sobre seu projeto')
    link_repositorio = StringField('Link Repositório', validators=[DataRequired()], description='Digite o Link para o Repositório')
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario', nullable=False))
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    botao_confirmacao = SubmitField('Enviar')

