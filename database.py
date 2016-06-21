from sqlalchemy import create_engine
from flask import Flask,session
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://toursanak:toursanak@localhost:5432/blog'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.secret_key = 'Hello@AmokCamSmallworld$Cambodia&*&'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
#upload url for feature images
app.config['UPLOAD_FOLDER'] = 'static/images/feature_images/'


def init_db():
    import BLOG.models
    Base.metadata.create_all(bind=engine)