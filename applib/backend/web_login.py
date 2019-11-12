
from flask import (Blueprint, url_for, request, 
                   render_template, redirect, flash,
                   session)

from applib.api.resp_handler import Response, RequestHandler, FormHandler
from applib.lib import helper  as h
from .bk_form import LoginForm
from werkzeug.security import check_password_hash, generate_password_hash
import json
from applib import model as m 

from sqlalchemy import func, extract, cast

from applib.lib import helper as h
from applib import model as m 

from functools import wraps 
from datetime import timedelta, date, datetime
import calendar


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
        today = datetime.now()
        
        _range = calendar.monthrange(today.year, today.month)
        
        first = today.replace(day=1) 

        last = date(today.year, today.month, _range[1])

        total_transact = db.query(m.Transactions.id).count()

        successful_transact = db.query(m.Transactions.trans_desc).filter(
                                m.Transactions.trans_desc =='successful').count()

        failed_transact = total_transact - successful_transact

        total_users=db.query(m.MobileUser.id).count()

        transact_montly_count = db.query(m.Transactions.id).filter(
            m.Transactions.date_created.between(first.date(), last)).count()

        users_montly_count = db.query(m.Transactions.id).filter(
            m.Transactions.date_created.between(first.date(), last)).count()
        
        




       
        transaction_qry ="""SELECT  sum(cast(transactions_table.trans_amount as INTEGER)) as amount, 
                                    strftime('%Y-%m', transactions_table.date_created) as dt,                                    
                                    service_list.label
                            
                            FROM transactions_table
                            LEFT JOIN service_items 
                                ON transactions_table.trans_type_id = service_items.id
                            LEFT JOIN service_list 
                                ON service_items.service_id = service_list.id
                            
                            WHERE strftime('%Y', transactions_table.date_created) = :Year
                            
                            GROUP BY dt  
                            ORDER By dt                          
                            

                        """  
        


        qry_data = db.execute(transaction_qry, {"Year": str(today.year)}).fetchall()

        series = []

        print('\n\n', qry_data, '\n\n')

 

        
        chart_range = [ "{}-{}".format(today.year, str(rng).zfill(2)) for rng in range(1,13, 1)]

        plot_data_collection = []
        service_names = db.query(m.ServicesMd.label).all()
           
        for x in service_names:
            series.append({"name": x.label, "data": []})

        
        for sec in chart_range:

            tmp_item = []
            for x in qry_data:                                 
                if sec == x.dt:
                    tmp_item.append(x.values())

            if not tmp_item:
                for plt in series:
                    plt['data'].append(0)

            else:

                for plt in series:
                    for y in tmp_item:
                        if y[2] == plt['name']:
                            plt['data'].append(y[0] or 0)
                            

    print('\n\n', series, '\n\n')

    return render_template('dashboard.html', 
                            plot_data=series,
                            total_transact=total_transact, 
                            transact_montly_count=transact_montly_count,
                            total_users=total_users,
                            users_montly_count=users_montly_count,
                            successful_transact=successful_transact,
                            failed_transact=failed_transact)



@app.route("/logout")
@is_active_session
def logout():
    
    # perform proper logout later on 

    del session['admin_username']
    # del session['admn_userid']

    return redirect(url_for('backend.login'))



def set_login_sessions(username):
    session["admin_username"] = username






