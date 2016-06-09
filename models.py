#from flask import Flask,session
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.sql.expression import text
#from sqlalchemy.exc import SQLAlchemyError
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy.orm import relationship
from slugify import slugify
from database import *
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://toursanak:toursanak@localhost:5432/blog'

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
# app.secret_key = 'Hello@AmokCamSmallworld$Cambodia&*&'
# db = SQLAlchemy(app)
 
#Create Database migrations
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
#Create the Post Class
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=  db.Column(db.String(100),nullable=True)
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
        self.name = name
    def add(self,category):
        db.session.add(category)
        return session_commit()
    def update(self):
        return session_commit()
    def delete(self,category):
        db.session.delete(category)
        return session_commit()
class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(255),nullable=True)
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
        self.description=description
    def add(self,page):
        db.session.add(page)
        return session_commit()
    def update(self):
        return session_commit()
    def delete(self,page):
        db.session.delete(page)
        return session_commit()
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255),nullable=True)
    description = db.Column(db.Text,nullable=True)
    feature_image=db.Column(db.String(200),nullable=True)
    slug=db.Column(db.String(255),nullable=True)
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
    def __init__(self, title, description, feature_image, category_id):
        self.title = title
        self.description = description
        self.feature_image = feature_image
        self.category_id = category_id
    def add(self,post):
        db.session.add(post)
        return session_commit()
    def update(self):
        return session_commit()
    def delete(self,post):
        db.session.delete(post)
        return session_commit()





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
 
# if __name__ == '__main__':
#     app.secret_key = 'Hello@AmokCamSmallworld$Cambodia&*&'
#     app.config['DEBUG'] = True
#     app.config['SESSION_TYPE'] = 'filesystem'
#     sess.init_app(app)
#     app.debug = True
#     manager.run()
#     app.run()



# @manager.command
# def init_db():
#     db.drop_all()
#     db.create_all()

#http://techarena51.com/index.php/one-to-many-relationships-with-flask-sqlalchemy/