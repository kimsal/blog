#!/usr/bin/env python
from database import *
import os.path as op
import os
import flask
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
template ="template-2016"
config=""
email=''
password=''
with open('config.txt','r') as f:
	config=str(f.read())
	data=config.split('\n')
	template=data[0].split('"')[1]
	limit=int(data[1].split('"')[1])
	email=data[2].split('"')[1]
	pwd=data[3].split('"')[1]
########## End Configuration ############
#### send mail ####
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = email,
	MAIL_PASSWORD = pwd
	)
mail=Mail(app)
#####################
#Middleware
@app.context_processor
def inject_dict_for_all_templates():
    return dict(searchform=SearchForm(),logined_name=request.cookies.get('blog_name'),template_name= template,categories = Category.query.filter_by(is_menu=1),pages = Page.query.filter_by(is_menu=1))
#========================================================
@auth.verify_token
def verify_token(token):
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
	form = UserMemberForm()
	if request.method == 'POST':
		email_form = request.form['email']
		password_form = request.form['password']
		user = UserMember.query.filter_by(email=email_form)
		if user.count()>0:
				#"set session"
				check=0
				for user_object in user:
					#return "{}".format(user_object.verify_password(password_form))
					if user_object.verify_password(password_form):
						response = make_response(redirect('/admin'))
						response.set_cookie("blog_id",str(user_object.id), expires=expire_date)
						response.set_cookie("blog_name",user_object.name, expires=expire_date)
						response.set_cookie("blog_email",user_object.email, expires=expire_date)
						response.set_cookie("blog_password",password_form, expires=expire_date)
						return response
					else:
						flash('Wrong user name or password !')
						return redirect(url_for("admin_login"))
		else:
			flash('Wrong user name or password !')
			return redirect(url_for("admin_login"))
	elif request.method == 'GET':
		#return str(request.cookies.get("blog_name"))
		if request.cookies.get("blog_name"):
			return redirect(url_for("admin_index"))
		return render_template('admin/form/login.html',form = form)
@app.route('/admin/logout', methods=['POST', 'GET'])
@app.route('/admin/logout/', methods=['POST', 'GET'])
@auth.login_required
def logout():
	response = make_response(redirect('/'))
	response.set_cookie("blog_id","", expires=0)
	response.set_cookie("blog_name","", expires=0)
	response.set_cookie("blog_email","", expires=0)
	response.set_cookie("blog_password","", expires=0)
	return response
@app.route('/admin/register', methods=['POST', 'GET'])
@app.route('/admin/register/', methods=['POST', 'GET'])
#@auth.login_required
def admin_register():
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
    form = PostForm()
    response = form.upload(endpoint=app)
    return response
@app.route('/admin')
@app.route('/admin/post')
@app.route('/admin/')
@app.route('/admin/<pagination>')
@auth.login_required
def admin_index(pagination=1):
	posts=Post.query.join(Category,Post.category_id == Category.id).order_by(Post.id.desc()).limit(limit).offset(int(int(int(pagination)-1)*limit))
	pagin=math.ceil((Post.query.join(Category,Post.category_id == Category.id).count())/limit)
	if((Post.query.count())%limit != 0 ):
		pagin=int(pagin+1)
	return render_template('admin/index.html' , posts = posts , pagin = int(pagin) , current_pagin = int(pagination))
@app.route('/admin/post/add', methods = ['GET', 'POST'])
@app.route('/admin/post/add/', methods = ['GET', 'POST'])
@app.route('/admin/post/edit/<slug>', methods = ['GET', 'POST'])
@app.route('/admin/post/edit/<slug>/', methods = ['GET', 'POST'])
@auth.login_required
def admin_post_add(slug=""):
	form = PostForm()
	categories = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
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
				filename=str(request.form['txt_temp_image'])
				if not slug:
		   			if file:
		   				obj=Post(request.form['title'],request.form['description'],request.form['category_id'],filename,request.cookies.get('blog_id'))
			        	status=Post.add(obj)
				        if not status:
				            flash("Post added was successfully")
				            return redirect(url_for('admin_index'))
				        else:
				        	flash("Fail to add post !")
				        	return redirect(url_for('admin_post_add'))
				elif slug:
		   			if not not file: 
			   			obj.update({"slug" : slugify(request.form['title']) , "title" : request.form['title'],'description':request.form['description'],'feature_image':filename })
		   				status = db.session.commit()
		   				if not status:
		   					flash("Post added was successfully")
		   					return redirect(url_for('admin_index'))
		   			for post in obj:
		   				tempFileName=post.feature_image
	   				filename=tempFileName
	   				obj.update({"slug" : slugify(request.form['title']) , "title" : request.form['title'],'description':request.form['description'],'feature_image':filename })
	   				status = db.session.commit()
	   				if not status:
	   					flash("Post updated was successfully")
	   					return redirect(url_for('admin_index'))
			        else:
			        	flash("Fail to update post!")
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
			return render_template('/admin/form/category.html',categories=categories,cat=cat, form = form)
@app.route('/admin/page/')
@app.route('/admin/page')
@app.route('/admin/page/<pagination>')
@auth.login_required
def admin_page(pagination=1):
	pages = Page.query.order_by(Page.id.desc())
	return render_template('admin/page.html', pages=pages)
@app.route('/admin/page/add', methods = ['GET', 'POST'])
@app.route('/admin/page/add/', methods = ['GET', 'POST'])
@app.route('/admin/page/edit/<slug>/', methods = ['GET', 'POST'])
@app.route('/admin/page/edit/<slug>', methods = ['GET', 'POST'])
@auth.login_required
def admin_page_add(slug=''):
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
	return render_template("/admin/template.html",templates_dir=templates_dir)
@app.route('/admin/template/<new_template>')
@app.route('/admin/template/<new_template>/')
def admin_choose_template(new_template):
	try:
		global config
		global template
		global limit
		global email
		with open('config.txt','w') as f:
			config=config.replace(template,new_template)
			f.write(config)
		###Read again:
		with open('config.txt','r') as f:
			config=str(f.read())
			data=config.split('\n')
			template=data[0].split('"')[1]
			limit=int(data[1].split('"')[1])
			email=data[2].split('"')[1]
			pwd=data[3].split('"')[1]
		flash("Template changed successfully.")
	except Exception as e:
		flash(str(e.message))
	return redirect(url_for('admin_index'))
@app.route('/admin/limit')
@app.route('/admin/limit/')
@app.route('/admin/limit/<number>', methods=['POST','GET'])
@app.route('/admin/limit/<number>/', methods=['POST','GET'])
def admin_limit(number=0):
	global config
	global template
	global limit
	global email
	if number==0:
		return render_template('/admin/limit.html',limit=limit)
	else:
		try:
			#return config
			with open('config.txt','w') as f:
				config=config.replace('limit="'+str(limit)+'"','limit="'+str(number)+'"')
				f.write(str(config))
			###Read again:
			with open('config.txt','r') as f:
				config=str(f.read())
				data=config.split('\n')
				template=data[0].split('"')[1]
				limit=int(data[1].split('"')[1])
				email=data[2].split('"')[1]
				pwd=data[3].split('"')[1]
			return jsonify({'success':"Ok" })
		except Exception as e:
			return jsonify({'success':str(e.message) })
@app.route('/admin/social')
@app.route('/admin/social/')
def admin_social():
	return render_template('/admin/social.html')
@app.route('/admin/menu')
@app.route('/admin/menu/')
def admin_menu(id=0,value=0):
	if request.method == 'GET':
		ps=Page.query.all()
		cats=Category.query.all()
		return render_template('/admin/menu.html',ps=ps,cats=cats)
@app.route('/admin/menu/<id>/<value>/<model>', methods=['POST', 'GET'])
@app.route('/admin/menu/<id>/<value>/<model>/', methods=['POST', 'GET'])
def admin_menu_set(id=0,value=0,model=''):
		if model=='category':
			try:
				category_object=Category.query.filter_by(id=id)
				category_object.update({"is_menu" : value })
				status = db.session.commit()
				if not status:
					return jsonify({'success':True}) 
				else:
					return jsonify({'success':False})
			except Exception as e:
				return jsonify({'success':str(e.message) })
		elif model=='page':
			try:
				page_object=Page.query.filter_by(id=id)
				page_object.update({"is_menu" : value })
				status = db.session.commit()
				if not status:
					return jsonify({'success':True}) 
				else:
					return jsonify({'success':False})
			except Exception as e:
				return jsonify({'success':str(e.message) })
@app.route('/recovery',methods=["POST","GET"])
@app.route('/recovery/',methods=["POST","GET"])
def verify_email():
	if request.method=="GET":
		return render_template('admin/verify-email.html')
	else:
		your_passowrd=''
		email_temp=request.form['email']
		users=UserMember.query.filter_by(email=email_temp)
		for usr in users:
			your_passowrd=usr.password2
			your_name=usr.name
		if your_passowrd!="":
			#send email
			try:
				global email
				#return email+":"+email_temp+":"+pwd
				msg = Message('Password recovery',sender=email,recipients=[email_temp])
				message_string='<div style="width:400px;border:2px solid blue;padding:10px;">Hello '+your_name+',<br/> Your password is: <b>'+your_passowrd+'</b></b> Thanks for choosing Amogli service.<br/></div>'
				msg.html = message_string
				mail.send(msg)				
				flash("Please check your email to recovery the password.")
				return redirect(url_for("admin_login"))
			except Exception as e:
				raise
				return str(e.message)
		else:
			#wrong email
			flash("Sorry, We couldn't find this email to recovery you password. It might wrong email address")
			return render_template('admin/verify-email.html')
			return "We couldn't find this email."
###########SEND MAIL##############
@app.route('/admin/email/group', methods = ['GET', 'POST'])
@app.route('/admin/email/group/', methods = ['GET', 'POST'])
# @app.route('/admin/email/group/<slug>', methods = ['GET', 'POST'])
# @app.route('/admin/email/group/<slug>/', methods = ['GET', 'POST'])
@app.route('/admin/email/group/<slug>/<action>', methods = ['GET', 'POST'])
@app.route('/admin/email/group/<slug>/<action>/', methods = ['GET', 'POST'])
@auth.login_required
def admin_mail_group(slug='',action=''):
	#slug is group name
	form = GroupForm()
	groups=Group.query.order_by(Group.published_at.desc()).all()
	if slug=='':
		if request.method=="GET":
			return render_template("admin/form/mailgroup.html",form=form,groups=groups)
		else:
			try:
				name = request.form['name']
				grp=Group(name)
				status=Group.add(grp)
				if not status:
					flash("Group Added successfully")
					return redirect(url_for('admin_mail_group'))
				else:
					flash("Error in adding Group !")
					return redirect(url_for('admin_mail_group'))
			except Exception as e:
				flask(e.message)
				return redirect(url_for("admin_mail_group"))
	else:
		#edit or delete
		if action=="edit":
			if request.method=="GET":
				return render_template("admin/form/mailgroup.html",form=form,groups=groups,name=slug)
			else:
				try:
					obj=Group.query.filter_by(name=slug)
					obj.update({"name" : request.form['name'] })
					status = db.session.commit()
					#status = obj.update({"name":request.form['name']})
					if not status:
						flash("Group updated successfully")
						return redirect(url_for('admin_mail_group'))
					else:
						flash("Error in updating group !")
						return redirect(url_for('admin_mail_group'))
				except Exception as e:
					flash(e.message)
					return redirect(url_for("admin_mail_group"))
		else:
			#delete group
			try:
				obj=Group.query.filter_by(name=slug).first()
				status = Group.delete(obj)
				if not status:
					flash("Group deleted successfully")
					return redirect(url_for('admin_mail_group'))
				else:
					flash("Error in deleting group !")
					return redirect(url_for('admin_mail_group'))
			except Exception as e:
				flash(e.message)
				return redirect(url_for('admin_mail_group'))
@app.route('/admin/mail', methods = ['GET', 'POST'])
@app.route('/admin/mail/', methods = ['GET', 'POST'])
@auth.login_required
def admin_mail():
	if request.method=="GET":
		return render_template("admin/form/maillist.html")
	else:
		return 'dd'
@app.route('/admin/email', methods = ['GET', 'POST'])
@app.route('/admin/email/', methods = ['GET', 'POST'])
@auth.login_required
def admin_email():
	if request.method=="GET":
		return render_template("admin/form/sendmail.html")
############## End send mail #####################
#End Middleware
#client
@app.errorhandler(404)
def page_not_found(e):
	return render_template(template+"/404.html")
@app.route('/')
@app.route('/pagin/<pagination>/')
@app.route('/pagin/<pagination>')
def index(pagination=1):
	global limit
	posts_top = Post.query.join(UserMember).order_by(Post.id.desc()).limit(3)
	posts_bottom = Post.query.order_by(Post.id.desc()).limit(10).offset(4)
	posts_bottom=Post.query.all()
	home_posts=Post.query.join(UserMember).order_by(Post.id.desc()).limit(limit)
	pagin=math.ceil((Post.query.count())/limit)
	return render_template(template+'/index.html',page_name='home',posts_top=posts_top,home_posts=home_posts,posts_bottom = posts_bottom,pagin=int(pagin),current_pagin=int(pagination))
@app.route('/<slug>')
@app.route('/<slug>/')
@app.route('/<slug>/<pagination>')
@app.route('/<slug>/<pagination>/')
#can be single and category page
def single(slug='',pagination=1):
	try:
		post_object=Post.query.filter_by(slug=slug)#.limit(1)
		if post_object.count()<=0:
			page_object=Page.query.filter_by(slug=slug)#.limit(1)
		if post_object.count()>0:
			for post in post_object:
				old_view=post.views
				post_object.update({"views" : (old_view+1) })
				status = db.session.commit()
		elif page_object.count()>0:
			return render_template(template+"/page.html",page_object=page_object)
		else:
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
			#return str(limit)
			return render_template(template+'/category.html',page_name='category',category_slug=category_slug,category_name=category_name,posts=posts,pagin=int(pagin),current_pagin=int(pagination))
	except:
		abort(404)
	return render_template(template+'/single.html',page_name='single',post_object=post_object)
@app.route('/category/<slug>')
@app.route('/category/<slug>/')
@app.route('/category/<slug>/<pagination>')
@app.route('/category/<slug>/<pagination>')
def category(slug='',pagination=1):
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
@app.route('/search', methods=['POST', 'GET'])
@app.route('/search/', methods=['POST', 'GET'])
@app.route('/sw', methods=['POST', 'GET'])
@app.route('/sw/', methods=['POST', 'GET'])
def search():
	search=(str(request.args['q']))#.split()
	search=search.replace(" ",'+')
	#return search
	if search=="":
		return redirect(url_for("index"))
	#return search
	query_result=(Post.query.filter((Post.title).match("'%"+search+"%'"),(Post.description).match("%'"+search+"'%"))).count()
	posts=Post.query.filter((Post.title).match("'%"+search+"%'"),(Post.description).match("%'"+search+"'%"))#.limit(limit).offset(int(int(int(limit)-1)*limit))
	return render_template(template+"/search.html",search=search,query_result=query_result,posts=posts)
@app.route('/admin/earn')
@app.route('/admin/earn/')
def admin_earn():
	return render_template("admin/earn.html")
#end client
if __name__ == '__main__':
	 app.run(debug = True,host='0.0.0.0')




#replace white space:
#http://docs.python-requests.org/en/master/user/quickstart/