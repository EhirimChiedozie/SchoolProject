from flask import Flask
from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a town value different from balablu'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
Base = declarative_base()
engine = create_engine('sqlite:///site.db',echo=True)
Session = sessionmaker(bind=engine)
session = Session()
app.config.from_object(__name__)
my_password = 'ogeapajgdeybegnu'
bcrypt = Bcrypt(app)
s = serializer(app.config['SECRET_KEY'])
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'chiedoziedavidehirim@gmail.com'
app.config['MAIL_PASSWORD'] = 'ogeapajgdeybegnu'
mail = Mail(app)
from school_web import routes