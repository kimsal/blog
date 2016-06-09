from flask import Flask, request,jsonify
#from flask_restful import Resource, Api,reqparse
from flask_restful import reqparse
from sqlalchemy import create_engine
from json import dumps
from database import *
from models import *
#import json
import datetime
#Create a engine for connecting to SQLite3.
#Assuming salaries.db is in your app root folder

#e = create_engine('sqlite:///salaries.db')

#app = Flask(__name__)
# blogApi = Api(app)

# class ApiPosts(Resource):
#     def get(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('pagin', type=str)
#         parser.add_argument('per_page', type=str)
#         parser.add_argument('slug', type=str)
#         pagin = parser.parse_args()['pagin']
#         per_page = parser.parse_args()['per_page']
#         slug = parser.parse_args()['slug']
#         if pagin is None:
#             pagin=1
#         if per_page is None:
#             per_page=20
        
#         #print "{}-{}".format(limit_from,limit_to)
#         pagin=int(pagin)-1
#         try:
#             if slug is None:
#                 #get all post and paginate
#                 posts=Post.query.order_by(Post.id.desc()).limit(per_page).offset(int(int(pagin)*int(per_page)))
#                 #serialized = json.dumps([c.to_Json() for c in posts])
#                 return posts
#             else:
#                 #single view page
#                 posts=Post.query.filter_by(slug=slug).limit(1)
#                 #serialized = json.dumps([c.to_Json() for c in posts])
#                 return posts
#         except:
#             raise
#             return ""
#         #We can have PUT,DELETE,POST here. But in our API GET implementation is sufficient
# class ApiCategory(Resource):
#     def get(self):
#         try:
#             category=Category.query.order_by(Category.id.desc())
#             serialized = json.dumps([c.to_Json() for c in category])
#             return serialized
#         except:
#             raise
#             return ""
#         #We can have PUT,DELETE,POST here. But in our API GET implementation is sufficient
# class ApiPage(Resource):
#     def get(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('slug', type=str)
#         slug = parser.parse_args()['slug']
#         if slug is None:
#             slug=None
#         try:
#             if slug is None:
#                 page=Page.query.order_by(Page.id.desc())
#                 serialized = json.dumps([c.to_Json() for c in page])
#                 return serialized
#             else:
#                 page=Page.query.filter_by(slug=slug).limit(1)
#                 serialized = json.dumps([c.to_Json() for c in page])
#                 return serialized
#         except: 
#             raise
#             return ""
# blogApi.add_resource(ApiPosts, '/api/post/getAll')
# blogApi.add_resource(ApiCategory, '/api/category/getAll')
# blogApi.add_resource(ApiPage, '/api/page/getAll')
# if __name__ == '__main__':
#      app.run(debug = True)


#http://blog.luisrei.com/articles/flaskrest.html