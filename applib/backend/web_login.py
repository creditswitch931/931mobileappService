
from flask import (Blueprint, url_for, request, render_template, redirect, flash)
from applib.api.resp_handler import Response, RequestHandler, FormHandler
from applib.lib import helper  as h
from .bk_form import LoginForm
from werkzeug.security import check_password_hash, generate_password_hash
import json

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('backend', __name__, url_prefix='/backend')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@app.route("/login", methods=['POST', 'GET'])
def login():

	form = LoginForm(request.form)

	error = None
	if request.method == 'POST' and form.validate():
		username = form.usr_name.data
		password = form.psd_wrd.data

		url = h.get_config("API", "login")
		login_content = {"username": username, "password": password, 
							"mac_address":"00:24:D7:2B:55:64"}
		req = RequestHandler(url, method=1, data=login_content)
		resp = req.send()

		for key, value in resp[1].items():
			if key == "statusCode":
				if value == "00":
					continue
			if key == "is_admin":
				if value == "1":
					return redirect(url_for('bk_cfg.service_view'))
				else:
					error = 'Incorrect Username/Password'
					flash(error)
					return redirect(url_for('.login'))

				
	return render_template('login.html', form=form)

@app.route("/admin")
def admin():
	
	# perform proper logout later on 

	return render_template('admin.html')

@app.route("/logout")
def logout_app():
	
	# perform proper logout later on 

	return redirect(url_for('  .login'))




