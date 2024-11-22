# Formuários
from datetime import datetime
from email.policy import default
from io import StringIO
from wsgiref.validate import validator

from email_validator import validate_email
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import URLField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, length

from ola_mundo import database
from ola_mundo.models import Usuario

# Adicionar RECAPTCHA
class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    botao_confirmacao = SubmitField('Fazer login')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError('Usuário inesistente, crie uma conta para continuar.')



class FormCriarConta(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()], description='Digite seu e-mail')
    username = StringField('Nome do Usuário', validators=[DataRequired(), Length(6, 60)], description='Digite um nome para seu Username')
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)], description='Digite uma senha segura.')
    confirmacao_senha = PasswordField('Confirmação de Senha', validators=[DataRequired(), EqualTo('senha')], description='Repita a mesma senha')
    botao_confirmacao = SubmitField('Criar conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail ja cadastrado, faça login para continuar')


class FormCategoria(FlaskForm):
    nome = StringField('Categoria', validators=[DataRequired()])
    botao_confirmacao = SubmitField('Enviar')


class FormFoto(FlaskForm):
    icone = FileField('Icone para o projeto', validators=[FileRequired()], description='Escolha uma imagem para ser o Icone.')
    nome = StringField('Nome do Projeto', validators=[DataRequired()])
    categoria = SelectField('Categoria', validators=[DataRequired()], coerce=int, choices=[], description='Selecione uma categoria para o projeto')
    descricao = StringField('Descrição do Projeto', validators=[DataRequired(), Length(1,400)], description='Diga em até 400 palavras sobre seu projeto')
    link_repositorio = StringField('Link: github.com/', validators=[DataRequired()], description='Digite o Link para o Repositório')
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario', nullable=False))
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    botao_confirmacao = SubmitField('Enviar')


class FormContato(FlaskForm):
    linkedin = StringField('Perfil do LinkedIn', validators=[DataRequired()], description='Link de destino para seu perfil do LinkedIn')
    github = StringField('Perfil do GitHub', validators=[DataRequired()], description='Link do perfil do LinkedIn')
    email = StringField('E-mail para contato', validators=[DataRequired()], description='E-mail seguro para contato')
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario', nullable=False))
    botao_confirmacao = SubmitField('Atualizar')