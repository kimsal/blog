# blog
https://github.com/flask-admin/flask-admin
http://flask-admin.readthedocs.io/en/latest/introduction/#working-with-the-built-in-templates
---------------------------------------------
#git clone git@github.com:flask-admin/flask-admin.git
//pip install flask-restful


pip install flaskckeditor




Url to learn:
http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xviii-deployment-on-the-heroku-cloud

ckeditor:
https://github.com/Still-not-satisfied-projects/flask-ckeditor/tree/master/examples/app


NOTE (must delete after it works):
from .forms import CKEditorForm

	@app.route('/ckupload/', methods=['POST', 'OPTIONS'])
	def ckupload():
	    """file/img upload interface"""
	    form = CKEditorForm()
	    response = form.upload(endpoint=app)
	    return response