
from flask import (Blueprint, url_for, request, 
                   render_template, redirect, flash,
                   session)

from applib.api.resp_handler import Response, RequestHandler, FormHandler
from applib.lib import helper  as h
from .bk_form import LoginForm
from werkzeug.security import check_password_hash, generate_password_hash
import json
from applib import model as m 

from sqlalchemy import func

from applib.lib import helper as h
from applib import model as m 

from functools import wraps 


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('backend', __name__, url_prefix='/backend')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

def is_active_session(func):

    @wraps(func)
    def verify_session(*args, **kwargs):

        if session.get('admin_username') is None:
            return redirect(url_for("backend.login"))
        
        return func(*args, **kwargs)

    return verify_session


@app.route("/login", methods=['POST', 'GET'])
def login():

    form = LoginForm(request.form)

    error = None
    if request.method == 'POST' and form.validate():
        username = form.usr_name.data
        password = form.psd_wrd.data

        user_name = h.get_config('LOGIN', 'username')
        pass_word = h.get_config('LOGIN', 'password')

        if username == user_name and password == pass_word:
            set_login_sessions(username)
            return redirect(url_for('backend.dashboard'))
        else:
            url = h.get_config("API", "login")
            login_content = {"username": username, "password": password, 
                                "mac_address": "1292999277"}
            req = RequestHandler(url, method=1, data=login_content)
            resp = req.send()

            if resp[1]['statusCode'] == "00" and resp[1]['is_admin'] == "1":
                set_login_sessions(username)
                
                return redirect(url_for('backend.dashboard'))
            else:
                error = 'Incorrect Username/Password'
                flash(error)

    return render_template('login.html', form=form)


@app.route("/dashboard")
@is_active_session
def dashboard():
    with m.sql_cursor() as db:
        data_count=db.query(func.count(m.Transactions.id)).scalar()
        


    # perform proper logout later on 

    return render_template('dashboard.html')

@app.route("/logout")
@is_active_session
def logout():
    
    # perform proper logout later on 

    del session['admin_username']
    # del session['admn_userid']

    return redirect(url_for('backend.login'))



def set_login_sessions(username):
    session["admin_username"] = username






