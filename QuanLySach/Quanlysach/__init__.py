from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary
from flask_babelex import Babel


app = Flask(__name__)
app.secret_key = 'jnskcmcmmkdsmva/,we;f;kal;,'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/labQuanlysachdb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 5
app.config['COMMENT_SIZE'] = 5

db = SQLAlchemy(app=app)

cloudinary.config(
    cloud_name = 'djpaz5u8i',
    api_key = '659466744891141',
    api_secret = 't69ADuvYRB5m02t-p4BOwjr99ag'
)

login = LoginManager(app=app)

babel = Babel(app=app)
@babel.localeselector
def get_locale():
    return 'vi'