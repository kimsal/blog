#from flask import Flask,session
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.sql.expression import text
#from sqlalchemy.exc import SQLAlchemyError
from database import *
from sqlalchemy.orm import relationship
from slugify import slugify
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://toursanak:toursanak@localhost:5432/blog'

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
# app.secret_key = 'Hello@AmokCamSmallworld$Cambodia&*&'
# db = SQLAlchemy(app)
 
#Create Database migrations
#Create the Post Class
from wtforms.widgets import * #TextArea
from wtforms import * #TextField, IntegerField, TextAreaField, SubmitField, RadioField,SelectField,validators, ValidationError
import wtforms.widgets.core
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

class UserMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100),nullable=True,unique=True)
    password = db.Column(db.String(100))
    created_at=db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp())
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
    def add(user):
        db.session.add(user)
        return db.session.commit()
    def update(self):
        return session_commit()
    def delete(user):
        db.session.delete(user)
        return session_commit()
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=  db.Column(db.String(100),nullable=True,unique=True)
    slug= db.Column(db.String(100),nullable=True)
    posts=db.relationship('Post', backref="category", lazy='dynamic')
    def get_absolute_url(self):
        return ('Category', (), {'slug': self.slug,'id': self.id,})
    def __str__(self):
        return self.name
    def to_Json(self):
        return dict(id=self.id,
            name=self.name,
            slug=self.slug
            )
    def __init__(self, name):
        self.slug=slugify(name)
        self.name =name
    def add(category):
        db.session.add(category)
        return db.session.commit()
    # def update(category,name):
    #     category.update({"slug" : slugify(name) , "name" : dict(name)})
    #     #db.session.commit()
    #     return session_commit()
    def delete(category):
        db.session.delete(category)
        return db.session.commit()
class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(255),nullable=True,unique=True)
    slug= db.Column(db.String(255),nullable=True)
    description = db.Column(db.Text,nullable=True)
    published_at= db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp())
    def get_absolute_url(self):
        return ('Page', (), {'slug': self.slug,'id': self.id,})
    def __str__(self):
        return self.title
    def to_Json(self):
        return dict(id=self.id,
            title=self.title,
            slug=self.slug,
            description=self.description,
            published_at="{}".format(self.published_at)
            )
    def __init__(self, title,description):
        self.title = title
        self.slug =slugify(title)
        self.description=description
    def add(page):
        db.session.add(page)
        return db.session.commit()
    # def update(self):
    #     return session_commit()
    def delete(page):
        db.session.delete(page)
        return db.session.commit()
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255),nullable=True,unique=True)
    description = db.Column(db.Text,nullable=True)
    feature_image=db.Column(db.String(200),nullable=True)
    slug=db.Column(db.String(255),nullable=True,unique=True)
    category_id=db.Column(db.Integer,db.ForeignKey('category.id'),nullable=True)
    published_at=db.Column(db.TIMESTAMP,server_default=db.func.current_timestamp())
    views = db.Column(db.Integer, nullable=True)
    def to_Json(self):
        return dict(id=self.id,
            title=self.title,
            description=self.description,
            feature_image=self.feature_image,
            slug=self.slug,
            category_id=self.category_id,
            published_at="{}".format(self.published_at),
            view=self.view
            )
    def __init__(self, title, description, category_id, feature_image):
        self.title = title
        self.description = description
        self.feature_image = feature_image
        self.category_id = category_id
        self.slug =slugify(title)
    def add(post):
        db.session.add(post)
        return db.session.commit()
    def update(self):
        return session_commit()
    def delete(post):
        db.session.delete(post)
        return session_commit()


#http://flask-admin.readthedocs.io/en/latest/advanced/

#http://charlesleifer.com/blog/how-to-make-a-flask-blog-in-one-hour-or-less/


        
    # def __init__(title, description,feature_image, slug,category,published_at):
    #         self.title = title
    #         self.description = Database
    #         self.feature_image=feature_image
    #         self.slug=slug
    #         self.category=category
    #         self.published_at=published_at
    #     def add(self,post):
    #         db.session.add(post)
    #         return session_commit()
    #     def update(self):
    #         return session_commit()
    #     def delete(self,post):
    #         db.session.delete(post)
    #         return session_commit()
    # def session_commit():
    #     try:
    #         db.session.commit()
    #     except SQLAlchemyError as e:
    #         reason=str(e)

#need when migrate database 
if __name__ == '__main__':
    app.secret_key = 'Hello@AmokCamSmallworld$Cambodia&*&'
    app.config['DEBUG'] = True
    app.config['SESSION_TYPE'] = 'filesystem'
   # sess.init_app(app)
    app.debug = True
    manager.run()
    app.run()



# @manager.command
# def init_db():
#     db.drop_all()
#     db.create_all()

#http://techarena51.com/index.php/one-to-many-relationships-with-flask-sqlalchemy/