
from flask import (Blueprint, url_for, request, render_template, redirect, flash)
from applib.api.resp_handler import Response, RequestHandler, FormHandler
from applib.lib import helper  as h
from .bk_form import LoginForm
from werkzeug.security import check_password_hash, generate_password_hash
import json
from applib import model as m 

from sqlalchemy import func

from applib.lib import helper  as h
from applib import model as m 


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

        user_name = h.get_config('LOGIN', 'username')
        pass_word = h.get_config('LOGIN', 'password')

        if username == user_name and password == pass_word:
            return redirect(url_for('bk_cfg.service_view'))
        else:
            url = h.get_config("API", "login")
            login_content = {"username": username, "password": password, 
                                "mac_address": "1292999277"}
            req = RequestHandler(url, method=1, data=login_content)
            resp = req.send()

            if resp[1]['statusCode'] == "00" and resp[1]['is_admin'] == "1":
                return redirect(url_for('bk_cfg.service_view'))
            else:
                error = 'Incorrect Username/Password'
                flash(error)

    return render_template('login.html', form=form)


@app.route("/dashboard")
def dashboard():
    with m.sql_cursor() as db:
        # data_count=db.query(func.count(m.Transactions.id)).scalar()
        pass
        

    # perform proper logout later on 

    return render_template('dashboard.html')

@app.route("/logout")
def logout_app():
    
    # perform proper logout later on 

    return redirect(url_for('  .login'))




