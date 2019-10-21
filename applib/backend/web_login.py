
from flask import (Blueprint, url_for, request, render_template)

from applib.lib import helper  as h
from .forms import LoginForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('login', __name__, url_prefix='/backend')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


# from flask_login import LoginManager

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.session_protection = "strong"
# login_manager.login_view = 'web_login.login'
# @login_manager.user_loader
# def load_user(user_id):
#     # since the user_id is just the primary key of our user table, 
#     # use it in the query for the user
#     return m.Users.query.get(user_id)


@app.route("/login", methods=['POST'])
def login():

	form = LoginForm(request.form)

	error = None
	if request.method == 'POST' and form.validate():
		username = form.usr_name.data
		password = form.psd_wrd.data

		with m.sql_cursor() as db:
			
			user = db.query(m.Users).filter(m.Users.username == username
											).first()

			if user is None:
				error = 'Incorrect Username/Password'

			elif not check_password_hash(user.password, password):
				error = 'Incorrect Username or Password'
			  
			if error is None:                
				session['user_id'] = user.id

				login_user(user)

				return redirect(url_for('admin.list'))

			flash(error)

	return render_template('login.html', form=form)


@app.route("/logout")
# @login_required
def logout_app():
    logout_user()
    return redirect(url_for('admin.login'))
