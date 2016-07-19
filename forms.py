#!/usr/bin/env python
from flask_wtf import Form
from wtforms import TextField,FileField,PasswordField, IntegerField, TextAreaField, SubmitField, RadioField,SelectField,validators, ValidationError
from flaskckeditor import CKEditor
class PostForm(Form,CKEditor):
   title = TextField("Title",[validators.Required("Please enter your title.")])
   description = TextAreaField("Description",[validators.Required("Please enter your description.")])   
   feature_image = FileField("Feature Image")
   category_id = SelectField('Category', choices=[], coerce=int)
   submit = SubmitField("Publish")

class CategoryForm(Form):
   name = TextField("Name",[validators.Required("Please enter category name.")])
class PageForm(Form,CKEditor):
	title = TextField("Title",[validators.Required("Please enter your title.")])
	description = TextAreaField("Description",[validators.Required("Please enter your description.")])
class UserMemberForm(Form):
   name = TextField("Name",[validators.Required("Please enter your name.")])
   email = TextField("Email",[validators.Required("Please enter your email.")])
   password = PasswordField("Password",[validators.Required("Please enter your password.")])
   submit = SubmitField("Login")
class SearchForm(Form):
    search = TextField("search")
class GroupForm(Form):
    name = TextField("Group Name")
class SearchForm(Form):
    q = TextField("Search ...")
class ContactForm(Form):
   name = TextField("Name",[validators.Required("Please enter your name.")])
   email = TextField("Email",[validators.Required("Please enter your email.")])