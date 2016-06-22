from flask_wtf import Form
from wtforms import TextField,FileField, IntegerField, TextAreaField, SubmitField, RadioField,SelectField,validators, ValidationError
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