
from flask import (Blueprint, url_for, request, render_template)

from applib.lib import helper  as h
from .bk_form import LoginForm
from werkzeug.security import check_password_hash, generate_password_hash

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('backend', __name__, url_prefix='/backend')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

@app.route("/login", methods=['POST'])
def login():

	form = LoginForm(request.form)

	error = None
	if request.method == 'POST' and form.validate():
		username = form.usr_name.data
		password = form.psd_wrd.data

		

	return render_template('login.html', form=form)



@app.route("/logout")
def logout_app():
	
	# perform proper logout later on 

    return redirect(url_for('  .login'))




