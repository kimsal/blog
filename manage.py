#from api import *
from database import *
import os.path as op
import os
import flask
#from views import *
from flask import abort,Flask,g, render_template,request,session,redirect,url_for,flash
from werkzeug import secure_filename
from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField,SelectField,validators, ValidationError
from flask_sijax import sijax
from flask.json import jsonify
import math
from models import *
from forms import *
from models import *
# import flask_sqlalchemy
# import flask_whooshalchemy

#Middleware
@app.context_processor
def inject_dict_for_all_templates():
    return dict(logined_name=request.cookies.get('blog_name'),template_name= template,categories = Category.query.all(),pages = Page.query.all())
#========================================================
@auth.verify_token
def verify_token(token):
	# g.current_user = UserMember.query.filter_by(token=token).first()
	# return g.current_user is not None
	user = UserMember.query.filter_by(email = request.cookies.get('blog_email'))
	if user.count()>0:
		for user_object in user:
			if user_object.verify_password(request.cookies.get('blog_password')):
				return True
	return False

@auth.error_handler
def goLoginPage():
	return redirect(url_for("admin_login"))
#================
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })
@app.route('/admin/login', methods=['POST', 'GET'])
@app.route('/admin/login/', methods=['POST', 'GET'])
def admin_login():
	# if session.get('logged_in'):
	# 	return redirect(url_for("admin_index"))
	form = UserMemberForm()
	if request.method == 'POST':
		email_form = request.form['email']
		password_form = request.form['password']
		user = UserMember.query.filter_by(email=email_form)
		#return "{}".format(user.count())
		if user.count()>0:
				#"set session"
				check=0
				for user_object in user:
					#return "{}".format(user_object.verify_password(password_form))
					if user_object.verify_password(password_form):
						# session['blog_id'] = user_object.id
						# session['blog_name'] = user_object.name
						# session['blog_email'] = user_object.email
						# session['blog_password'] = password_form

						response = make_response(redirect('/admin'))
						response.set_cookie("blog_id",str(user_object.id), expires=expire_date)
						response.set_cookie("blog_name",user_object.name, expires=expire_date)
						response.set_cookie("blog_email",user_object.email, expires=expire_date)
						response.set_cookie("blog_password",password_form, expires=expire_date)
						#print request.cookies.get('blog_name')
						#session['logged_in'] = True
						#token = user_object.generate_auth_token()
						#return token
						#check=True
						return response
						#return redirect(url_for('admin_index'))
					else:
						flash('Wrong user name or password !')
						return redirect(url_for("admin_login"))
		else:
			flash('Wrong user name or password !')
			return redirect(url_for("admin_login"))
	elif request.method == 'GET':
		if request.cookies.get("blog_name"):
			return redirect(url_for("admin_index"))
		return render_template('admin/form/login.html',form = form)
@app.route('/admin/logout', methods=['POST', 'GET'])
@app.route('/admin/logout/', methods=['POST', 'GET'])
@auth.login_required
def logout():
	#return session.get['blog_email']
	# session['blog_email'] = ""
	# session['blog_password'] = ""
	# session['logged_in'] = False
	response = make_response(redirect('/'))
	response.set_cookie("blog_id","", expires=0)
	response.set_cookie("blog_name","", expires=0)
	response.set_cookie("blog_email","", expires=0)
	response.set_cookie("blog_password","", expires=0)
	#return redirect(url_for("index"))
	return response
	#return redirect(url_for('admin_login'),401)
@app.route('/admin/register', methods=['POST', 'GET'])
@app.route('/admin/register/', methods=['POST', 'GET'])
#@auth.login_required
def admin_register():
	# if not session.get('logged_in'):
	# 	return redirect(url_for("admin_login"))
	form = UserMemberForm()
	if request.method == 'POST':
		user=UserMember(request.form['name'],request.form['email'],request.form['password'])
		user.hash_password(request.form['password'])
		try:
			status=UserMember.add(user)
			if not status:
				flash("User Added successfully")
				return redirect(url_for('admin_login'))
			else:
				flash("Error in adding User !")
				return redirect(url_for('admin_register'))	
		except:
			flash("Error in adding User !")
			return redirect(url_for('admin_register'))

	return render_template('admin/form/register.html', form = form)

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
@auth.login_required
def admin_index(pagination=1):
	# if not session.get('logged_in'):
	# 	return redirect(url_for("admin_login"))
	limit=20
	posts=Post.query.join(Category,Post.category_id == Category.id).order_by(Post.id.desc()).limit(limit).offset(int(int(int(pagination)-1)*limit))
	pagin=math.ceil((Post.query.join(Category,Post.category_id == Category.id).count())/limit)
	if((Post.query.count())%limit != 0 ):
		pagin=int(pagin+1)
	#return "{}".format(posts)
	return render_template('admin/index.html' , posts = posts , pagin = int(pagin) , current_pagin = int(pagination))
@app.route('/admin/post/add', methods = ['GET', 'POST'])
@app.route('/admin/post/add/', methods = ['GET', 'POST'])
@app.route('/admin/post/edit/<slug>', methods = ['GET', 'POST'])
@app.route('/admin/post/edit/<slug>/', methods = ['GET', 'POST'])
@auth.login_required
def admin_post_add(slug=""):
	# if not session.get('logged_in'):
	# 	return redirect(url_for("admin_login"))
	form = PostForm()
	#form_overrides = dict(text=CKTextAreaField)
	categories = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
	#form = RecipeForm(request.form)
	form.category_id.choices = categories
	if request.method == 'POST':
		try:
			if form.validate() == False:
		   		flash('All fields are required.')
		   		return redirect(url_for('admin_post_add'))
		   	else:
		   		obj=Post.query.filter_by(slug=slug)
		   		now = str(datetime.now())
				now= now.replace(':',"",10).replace(' ','',4).replace('.','',5).replace('-','',5)
		   		result = request.form
				file = request.files['feature_image']
				filename = secure_filename(file.filename)
				#return str(result)+" : "+str(file)+" : "+str(filename)
		   		if not slug:
		   			if file:
		   				file.save(os.path.join(app.config['UPLOAD_FOLDER'], now+"-"+filename))
			        	#return str(result)+":"+str(file)+":"+str(filename)
			        	obj=Post(request.form['title'],request.form['description'],request.form['category_id'],(now+"-"+filename),request.cookies.get('blog_id'))
			        	
			        	status=Post.add(obj)
				        if not status:
				            flash("Post added was successfully")
				            return redirect(url_for('admin_index'))
				        else:
				        	flash("Fail to add post !")
				        	return redirect(url_for('admin_post_add'))
				 #   	#else:
					# flash("Fail to upload feature image !")
		   # 			return render_template('admin/form/post.html', form = form)
		   		elif slug:
		   			#upload feature image
		   			#return str(not not file)
		   			if not not file: 
			   			#upload imagesif len(filename)>0:
		   				file.save(os.path.join(app.config['UPLOAD_FOLDER'], (now+"-"+filename)))
		   				obj.update({"slug" : slugify(request.form['title']) , "title" : request.form['title'],'description':request.form['description'],'feature_image':(now+"-"+filename) })
		   				status = db.session.commit()
		   				if not status:
		   					flash("Post added was successfully")
		   					return redirect(url_for('admin_index'))
				        # else:
				        # 	flash("Fail to update post 2 !")
				        # 	return redirect(url_for('admin_index'))
				    #else:
					    #don't upload image
					    #update row
		   			for post in obj:
		   				tempFileName=post.feature_image
	   				filename=tempFileName
	   				obj.update({"slug" : slugify(request.form['title']) , "title" : request.form['title'],'description':request.form['description'],'feature_image':str(filename) })
	   				status = db.session.commit()
	   				if not status:
	   					flash("Post updated was successfully 1")
	   					return redirect(url_for('admin_index'))
			        else:
			        	flash("Fail to update post 111 !")
			        	return redirect(url_for('admin_index'))

		except Exception  as e:
			flash(str(e.message))
			return redirect(url_for("admin_post_add"))

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
@app.route('/admin/category/edit/<slug>/', methods = ['GET', 'POST'])
@auth.login_required
def admin_category_add(slug=""):
	# if not session.get('logged_in'):
	# 	return redirect(url_for("admin_login"))
	form = CategoryForm()
	categories= Category.query.order_by(Category.name)
	if request.method == 'POST':
		try:
			if form.validate() == False:
		   		flash('please input category name !')
		   		return redirect(url_for('admin_category_add'))
	   		if not slug:
	   			#add category
		   		obj=Category(request.form['name'])
		   		status=Category.add(obj)
				if not status:
					flash("Category Added successfully")
					return redirect(url_for('admin_category_add'))
				else:
					flash("Error in adding page !")
					return redirect(url_for('admin_category_add'))	
			elif slug:
				#update category
	   			Category.query.filter_by(slug = slug).update({"slug" : slugify(request.form['name']) , "name" : request.form['name'] })
	   			status = db.session.commit()
	   			if not status:
	   				flash("Category updated successfully")
	   				return redirect(url_for('admin_category_add'))
		        else:
		        	flash("Error in updating category !")
		        	return redirect(url_for('admin_category_add'))
		except Exception as e:
			flash(str(e.message))
			return redirect(url_for("admin_category_add"))
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
@auth.login_required
def admin_page(pagination=1):
	# if not session.get('logged_in'):
	# 	return redirect(url_for("admin_login"))
	pages = Page.query.order_by(Page.id.desc())
	return render_template('admin/page.html', pages=pages)

@app.route('/admin/page/add', methods = ['GET', 'POST'])
@app.route('/admin/page/add/', methods = ['GET', 'POST'])
@app.route('/admin/page/edit/<slug>/', methods = ['GET', 'POST'])
@app.route('/admin/page/edit/<slug>', methods = ['GET', 'POST'])
@auth.login_required
def admin_page_add(slug=''):
	# if not session.get('logged_in'):
	# 	return redirect(url_for("admin_login"))
	form = PageForm()
	if request.method == 'POST':
		try:
			if form.validate() == False:
		   		flash('All fields are required !'	)
		   		return redirect(url_for('admin_page_add'))
		   	else:
		   		if not slug:
		   			#add new
			   		obj=Page(request.form['title'],request.form['description'])
			   		status=Page.add(obj)
					if not status:
						flash("Page Added successfully")
						return redirect(url_for('admin_page'))
					else:
						flash("Error in adding page !")
						return redirect(url_for('admin_page_add'))
		   		elif slug:
		   			#status=Category.update(obj)
		   			Page.query.filter_by(slug = slug).update({"slug" : slugify(request.form['title']) , "title" : request.form['title'] , "description" : request.form['description']})
		   			status = db.session.commit()
		   			if not status:
		   				flash("Page updated successfully")
		   				return redirect(url_for('admin_page'))
			        else:
			        	flash("Error !")
			        	return redirect(url_for('admin_page_add'))
		except Exception as e:
			flash(str(e.message))
			return redirect(url_for("admin_page_add"))
	else:
		if not slug:
			return render_template('/admin/form/page.html', form = form)
		else:
			page= Page.query.filter_by(slug=slug)
			return render_template('/admin/form/page.html',page=page, form = form)
@app.route('/admin/page/delete/<slug>/')
@app.route('/admin/page/delete/<slug>')
@auth.login_required
def admin_page_delete(slug=''):
	# if not session.get('logged_in'):
	# 	return redirect(url_for("admin_login"))
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
@auth.login_required
def admin_category_delete(slug):
	# if not session.get('logged_in'):
	# 	return redirect(url_for("admin_login"))	
	obj1 = Category.query.filter_by(slug=slug).first()
	try:
		status = Category.delete(obj1)
		flash('Deleted successful.')
		return redirect(url_for('admin_category_add'))
	except:
		flash('Fail to delete !')
		return redirect(url_for('admin_category_add'))

@app.route('/admin/post/delete/<slug>')
@app.route('/admin/post/delete/<slug>/')
@auth.login_required
def admiin_post_delete(slug=''):
	obj = Post.query.filter_by(slug=slug).first()
	try:
		status = Post.delete(obj)
		flash('Post deleted successful.')
		return redirect(url_for('admin_index'))
	except Exception as e:
		flash(str(e.message))
		return redirect(url_for('admin_index'))
@app.route('/admin/template')
@app.route('/admin/template/')
@auth.login_required
def admin_template():
	templates_dir=os.listdir(os.path.join(app.template_folder))
	templates_dir.remove("admin")
	#return "{}".format(templates_dir)
	return render_template("/admin/template.html",templates_dir=templates_dir)
#End Middleware




#client
@app.errorhandler(404)
def page_not_found(e):
	return render_template(template+"/404.html")
@app.route('/')
def index():
	posts_top = Post.query.order_by(Post.id.desc()).limit(4)
	posts_bottom = Post.query.order_by(Post.id.desc()).limit(60).offset(5)
	#return "{}".format(posts_top)
	return render_template(template+'/index.html',page_name='home',posts_top=posts_top,posts_bottom = posts_bottom)
@app.route('/<slug>')
@app.route('/<slug>/')
@app.route('/<slug>/<pagination>')
@app.route('/<slug>/<pagination>/')
#can be single and category page
def single(slug='',pagination=1):
	try:
		post_object=Post.query.filter_by(slug=slug)#.limit(1)
		page_object=Page.query.filter_by(slug=slug)#.limit(1)
		if post_object.count()>0:
			#return "1"
			for post in post_object:
				old_view=post.views
				post_object.update({"views" : (old_view+1) })
				status = db.session.commit()
		elif page_object.count()>0:
			return render_template("/template-2016/page.html",page_object=page_object)
		else:
			#return "2"
			limit=10
			category=Category.query.filter_by(slug=slug)
			cat_id=""
			category_name="None"
			category_slug=""
			for cat in category:
				cat_id=cat.id
				category_name=cat.name
				category_slug=cat.slug
			if cat_id == "":
				abort(404)
			posts=Post.query.filter_by(category_id=cat_id).order_by(Post.id.desc()).limit(limit).offset(int(int(int(pagination)-1)*limit))
			pagin=math.ceil((Post.query.filter_by(category_id=cat_id).count())/limit)
			if(math.ceil(Post.query.filter_by(category_id=cat_id).count())%limit != 0 ):
				pagin=int(pagin+1)
			return render_template(template+'/category.html',page_name='category',category_slug=category_slug,category_name=category_name,posts=posts,pagin=int(pagin),current_pagin=int(pagination))
	except:
		#return e.message
		abort(404)
	return render_template(template+'/single.html',page_name='single',post_object=post_object)
@app.route('/category/<slug>')
@app.route('/category/<slug>/')
@app.route('/category/<slug>/<pagination>')
@app.route('/category/<slug>/<pagination>')
def category(slug='',pagination=1):
	limit=10
	category=Category.query.filter_by(slug=slug)
	cat_id=""
	category_name="None"
	category_slug=""
	for cat in category:
		cat_id=cat.id
		category_name=cat.name
		category_slug=cat.slug
	if cat_id == "":
		abort(404)
	posts=Post.query.filter_by(category_id=cat_id).order_by(Post.id.desc()).limit(limit).offset(int(int(int(pagination)-1)*limit))
	pagin=math.ceil((Post.query.filter_by(category_id=cat_id).count())/limit)
	if(math.ceil(Post.query.filter_by(category_id=cat_id).count())%limit != 0 ):
		pagin=int(pagin+1)
	return render_template(template+'/category.html',page_name='category',category_slug=category_slug,category_name=category_name,posts=posts,pagin=int(pagin),current_pagin=int(pagination))
@app.route('/search/<slug>', methods=['POST', 'GET'])
@app.route('/search/<slug>/', methods=['POST', 'GET'])
def search(slug):
	#whooshalchemy.whoosh_index(app, Post)
	results = "Post.query.whoosh_search('cool')"
	return "{}".format(results)
#end client
if __name__ == '__main__':
	 app.run(debug = True)




#replace white space:
#http://docs.python-requests.org/en/master/user/quickstart/