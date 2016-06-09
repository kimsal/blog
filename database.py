from sqlalchemy import create_engine
from flask import Flask,session
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://toursanak:toursanak@localhost:5432/blog'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.secret_key = 'Hello@AmokCamSmallworld$Cambodia&*&'
db = SQLAlchemy(app)

def init_db():
    import BLOG.models
    Base.metadata.create_all(bind=engine)