from models import *
from api import *
import os.path as op
#from views import *
from models import *
from flask import Flask,g, render_template,request,session,redirect,url_for,flash
from werkzeug import secure_filename
import os
import flask
from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField,SelectField,validators, ValidationError
from flask_sijax import sijax
from database import *
from api import *
from flask.json import jsonify
import math
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
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
@app.route('/admin')
@app.route('/admin/')
@app.route('/admin/<pagin>')
def admin_index(pagin=1):
	limit=2
	#return '{}'.format(pagin)
	posts=Post.query.order_by(Post.id.desc()).limit(limit).offset(int(int(int(pagin)-1)*limit))
	pagin=math.ceil((Post.query.count())/limit)
	if((Post.query.count())%limit != 0 ):
		pagin=int(pagin+1)
	return render_template('admin/index.html',pagin = pagin, posts = posts)
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


#http://docs.python-requests.org/en/master/user/quickstart/