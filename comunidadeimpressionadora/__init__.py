from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__) #Cria o site

app.config['SECRET_KEY'] = '79838058486660f0731313e36d946399'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)

bcrypt = Bcrypt(app) #Fazendo isso só o site consegue descriptografar a senha do usuario
login_manager = LoginManager(app)

from comunidadeimpressionadora import routes