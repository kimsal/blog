#from api import *
from database import *
import os.path as op
import os
import flask
#from views import *
from flask import Flask,g, render_template,request,session,redirect,url_for,flash
from werkzeug import secure_filename
from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField,SelectField,validators, ValidationError
from flask_sijax import sijax
from api import *
from flask.json import jsonify
import math
from models import *
from forms import *
from models import *

#Middleware
def login_required(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return fn(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return inner
@app.route('/login/', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') or request.form.get('next')
    if request.method == 'POST' and request.form.get('password'):
        password = request.form.get('password')
        if password == app.config['ADMIN_PASSWORD']:
            session['logged_in'] = True
            session.permanent = True  # Use cookie to store session.
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('admin_index'))
        else:
            flash('Incorrect password.', 'danger')
    return render_template('admin/login.html', next_url=next_url)

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('login'))
    return render_template('logout.html')

@app.route('/ckupload/', methods=['POST', 'OPTIONS'])
def ckupload():
    """file/img upload interface"""
    form = PostForm()
    response = form.upload(endpoint=app)
    return response
@app.route('/admin')
@app.route('/admin/post')
@app.route('/admin/')
@app.route('/admin/<pagination>')
def admin_index(pagination=1):
	limit=2
	posts=Post.query.join(Category,Post.category_id == Category.id).order_by(Post.id.desc()).limit(limit).offset(int(int(int(pagination)-1)*limit))
	pagin=math.ceil((Post.query.count())/limit)
	if((Post.query.count())%limit != 0 ):
		pagin=int(pagin+1)
	#return "{}".format(posts)
	return render_template('admin/index.html' , posts = posts , pagin = int(pagin) , current_pagin = int(pagination))
@app.route('/admin/post/add', methods = ['GET', 'POST'])
@app.route('/admin/post/add/', methods = ['GET', 'POST'])
@app.route('/admin/post/edit/<slug>', methods = ['GET', 'POST'])
@app.route('/admin/post/edit/<slug>/', methods = ['GET', 'POST'])
def admin_post_add(slug=""):
	form = PostForm()
	#form_overrides = dict(text=CKTextAreaField)
	categories = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
	#form = RecipeForm(request.form)
	form.category_id.choices = categories
	if request.method == 'POST':
		if form.validate() == False:
	   		flash('All fields are required.')
	   		return redirect(url_for('admin_post_add'))
	   	else:
	   		#code to save and flask success
	   		result = request.form
			file = request.files['feature_image']
			filename = secure_filename(file.filename)
	        if file:
	        	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	        	obj=Post(request.form['title'],request.form['description'],request.form['category_id'],filename)
	        	#return "{}".format(file)	
		        status=Post.add(obj)
		        if not status:
		            flash("Post added was successfully")
		            return redirect(url_for('admin_index'))
		        else:
	   				flash("Fail to post !")
	   				return redirect(url_for('admin_post_add'))
	   		
	        else:
	   			flash("Fail to upload feature image !")
	   			return render_template('admin/post.html', form = form)
	elif request.method == 'GET':
		if slug:
			post=Post.query.filter_by(slug=slug)
			return render_template('admin/form/post.html', post = post, form = form)
		else:
			return render_template('admin/form/post.html', form = form)
@app.route('/admin/category', methods = ['GET', 'POST'])
@app.route('/admin/category/', methods = ['GET', 'POST'])
@app.route('/admin/category/add', methods = ['GET', 'POST'])
@app.route('/admin/category/add/', methods = ['GET', 'POST'])
@app.route('/admin/category/edit/<slug>', methods = ['GET', 'POST'])
def admin_category(slug=''):
	form = CategoryForm()
	categories= Category.query.order_by(Category.name)
	if request.method == 'POST':
		if form.validate() == False:
	   		flash('Please insert category name'	)
	   		return redirect(url_for('admin_category'))
	   	else:
	   		if slug:
	   			#update row
	   			obj=Category.query.filter_by(slug=slug).first()
	   			#status=Category.update(obj)
	   			Category.query.filter_by(slug = slug).update({"slug" : slugify(request.form['name']) , "name" : request.form['name']})
	   			status = db.session.commit()
	   			if not status:
	   				flash("update successfully")
	   				return redirect(url_for('admin_category'))
		        else:
		        	flash("Error !")
		        	return redirect(url_for('admin_category'))
	   		if not slug:
	   			#add new category
	   			obj=Category(request.form['name'])
		        status=Category.add(obj)
		        if not status:
		            flash("Added successfully")
		            return redirect(url_for('admin_category'))
		        else:
		        	flash("Error !")
		        	return redirect(url_for('admin_category'))
	elif request.method == 'GET':
		if not slug:
			return render_template('/admin/form/category.html',categories=categories, form = form)
		else:
			cat= Category.query.filter_by(slug=slug)
			#return redirect(url_for('admin_category'))
			return render_template('/admin/form/category.html',categories=categories,cat=cat, form = form)
@app.route('/admin/page/')
@app.route('/admin/page')
@app.route('/admin/page/<pagination>')
def admin_page(pagination=1):
	pages = Page.query.order_by(Page.id.desc())
	return render_template('admin/page.html', pages=pages)

@app.route('/admin/page/add', methods = ['GET', 'POST'])
@app.route('/admin/page/add/', methods = ['GET', 'POST'])
@app.route('/admin/page/edit/<slug>/', methods = ['GET', 'POST'])
@app.route('/admin/page/edit/<slug>', methods = ['GET', 'POST'])
def admin_page_add(slug=''):
	form = PageForm()
	if request.method == 'POST':
		if form.validate() == False:
	   		flash('Invalid input !'	)
	   		return redirect(url_for('admin_page_add'))
	   	else:
	   		if slug:
	   			#update row
	   			#obj=Page.query.filter_by(slug=slug).first()
	   			#status=Category.update(obj)
	   			Page.query.filter_by(slug = slug).update({"slug" : slugify(request.form['title']) , "title" : request.form['title'] , "description" : request.form['description']})
	   			status = db.session.commit()
	   			if not status:
	   				flash("Page updated successfully")
	   				return redirect(url_for('admin_page'))
		        else:
		        	flash("Error !")
		        	return redirect(url_for('admin_page_add'))
		    
	   		if not slug:
		   		obj=Page(request.form['title'],request.form['description'])
		   		status=Page.add(obj)
				if not status:
					flash("Page Added successfully")
					return redirect(url_for('admin_page'))
				else:
					flash("Error in adding page !")
					return redirect(url_for('admin_page_add'))
	else:
		if not slug:
			return render_template('/admin/form/page.html', form = form)
		else:
			page= Page.query.filter_by(slug=slug)
			return render_template('/admin/form/page.html',page=page, form = form)
@app.route('/admin/page/delete/<slug>/')
@app.route('/admin/page/delete/<slug>')
def admin_page_delete(slug=''):
	obj1 = Page.query.filter_by(slug=slug).first()
	try:
		status = Page.delete(obj1)
		flash('Deleted successful.')
		return redirect(url_for('admin_page'))
	except:
		flash('Fail to delete !')
		return redirect(url_for('admin_page'))
@app.route('/admin/category/delete/<slug>')
@app.route('/admin/category/delete/<slug>/')
def admin_category_delete(slug):	
	obj1 = Category.query.filter_by(slug=slug).first()
	try:
		status = Category.delete(obj1)
		flash('Deleted successful.')
		return redirect(url_for('admin_category'))
	except:
		flash('Fail to delete !')
		return redirect(url_for('admin_category'))
	


# @app.route('/admin/category/')
# @app.route('/admin/category')
# def admin_page():
# 	categories = Category.query.order_by(Page.id.desc())
# 	return render_template('admin/category.html', categories=categories)
#End Middleware




#client
@app.route('/')
def index():
	return render_template('index.html')
@app.route('/<slug>')
def single(slug):
	return render_template('single.html')
#end client
if __name__ == '__main__':
	 app.run(debug = True)



#replace white space:
#http://docs.python-requests.org/en/master/user/quickstart/