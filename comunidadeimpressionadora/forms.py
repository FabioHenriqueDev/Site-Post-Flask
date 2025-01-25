from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError # DataRequired eh pra deixar o campo obrigatório
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user

class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(4, 20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 15)])
    confirmacao = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha'), Length(6, 15)])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()

        if usuario:
            raise ValidationError('E-mail ja cadastrado. Cadastre se com outro email eu faça login para continuar')

    def validate_username(self, username):
        nome_repitido = Usuario.query.filter_by(username=username.data).first()

        if nome_repitido:
            raise ValidationError('Esse nome de usuário ja existe. Por favor digite outro')

class FormLogin(FlaskForm):
    email_login = StringField('E-mail', validators=[DataRequired(), Email()])
    senha_login = PasswordField('Senha', validators=[DataRequired(), Length(6, 15)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(4, 20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    botao_submit_editarperfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):

        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Ja existe um usuário com esse E-mail. Por favor digite outro')


    def validate_username(self, username):
        if current_user.username != username.data:
            nome_repitido = Usuario.query.filter_by(username=username.data).first()
            if nome_repitido:
                raise ValidationError('Ja existe um usuário com esse Username. Por favor digite outro')
