
from flask import (Blueprint, url_for, request, 
                   render_template, redirect, flash,
                   session)

from applib.api.resp_handler import Response, RequestHandler, FormHandler
from applib.lib import helper  as h
from .bk_form import LoginForm
from werkzeug.security import check_password_hash, generate_password_hash
import json
from applib import model as m 

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

    today = datetime.now()        
    _range = calendar.monthrange(today.year, today.month)
    
    first = today.replace(day=1) 

    last = date(today.year, today.month, _range[1])


    sale_report_annual = """SELECT  sum(cast(transactions_table.trans_amount as INTEGER)) as amount, 
                                    strftime('%Y-%m', transactions_table.date_created) as dt,                                    
                                    service_list.label                            
                            FROM transactions_table
                            LEFT JOIN service_items 
                                ON transactions_table.trans_type_id = service_items.id
                            LEFT JOIN service_list 
                                ON service_items.service_id = service_list.id
                            
                            WHERE strftime('%Y', transactions_table.date_created) = :Year
                            AND  transactions_table.trans_type_id is not Null
                            AND transactions_table.trans_code = '0'

                            GROUP BY dt, service_list.label
                            ORDER By dt                          
                            
                        """  
        
    sales_dist_month = """SELECT  sum(cast(transactions_table.trans_amount as INTEGER)) as amount, 
                                strftime('%Y-%m', transactions_table.date_created) as dt,                                    
                                service_list.label 
                        
                        FROM transactions_table
                        LEFT JOIN service_items 
                            ON transactions_table.trans_type_id = service_items.id
                        LEFT JOIN service_list 
                            ON service_items.service_id = service_list.id
                        
                        WHERE strftime('%Y-%m', transactions_table.date_created) = :range
                         AND  transactions_table.trans_type_id is not Null
                         AND transactions_table.trans_code = '0'

                        GROUP BY dt , service_list.label
                        ORDER By dt                      
                        
                    """

    payment_distribution = """SELECT transactions_table.trans_code as status,
                                sum(cast(transactions_table.trans_amount as INTEGER)) as amount,
                                count(transactions_table.trans_code) as count
                            FROM transactions_table
                            WHERE strftime('%Y-%m', transactions_table.date_created) = :range
                            AND  transactions_table.trans_type_id is Null
                            GROUP BY status
                    """

    transactions_sql = """SELECT transactions_table.trans_code as status,
                                sum(cast(transactions_table.trans_amount as INTEGER)) as amount,
                                count(transactions_table.trans_code) as count
                            FROM transactions_table
                            WHERE strftime('%Y-%m', transactions_table.date_created) = :range
                            AND  transactions_table.trans_type_id is not Null
                            GROUP BY status
                    """



    with m.sql_cursor() as db:    
        

        cur_trans = db.execute(transactions_sql, {"range": "{}-{}".format(today.year, today.month)}).fetchall()
        
        failed_trans, success_trans = 0, 0 
        success_trans_amount = 0

        for x in cur_trans:
            if x.status == '0':
                success_trans = x.count
                success_trans_amount = x.amount
            elif x.status == '1':
                failed_trans = x.count 
        

        users_obj = db.query(m.MobileUser).filter(m.MobileUser.active == 1)
        total_users = users_obj.count()
        newly_created_users = users_obj.filter(
                                            m.MobileUser.date_created.between(first.date(), last)
                                            ).count() 
        qry_data = db.execute(sale_report_annual, {"Year": str(today.year)}).fetchall()
        
        sales_dist_data = db.execute(sales_dist_month, {"range": "{}-{}".format(today.year, today.month)}).fetchall()
        payments_result = db.execute(payment_distribution, {"range": "{}-{}".format(today.year, today.month)}).fetchall()             
    
        payment_info = dict(
            total_online_payment = 0,
            total_online_count = 0,
            total_online_payment_failed = 0,
            total_online_count_failed = 0
        )

        for pay in payments_result:
            if pay.status == '0':
                payment_info['total_online_payment'] = pay.amount 
                payment_info['total_online_count'] = pay.count 

            elif pay.status == '1':
                payment_info['total_online_payment_failed'] = pay.amount
                payment_info['total_online_count_failed'] = pay.count 


        service_names = db.query(m.ServicesMd.label).all()
        service_name_list = [x.label for x in service_names]
        
        series = [] 
        for x in service_name_list:
            series.append({"name": x, "data": [ x*0 for x in range(1,13, 1)]})
        
        index_count = 0 
        chart_range = ["{}-{}".format(today.year, str(rng).zfill(2)) for rng in range(1,13, 1)]
        for sec in chart_range:

            tmp_item = []
            for x in qry_data:                                 
                if sec == x.dt:
                    tmp_item.append(x.values())

            if tmp_item:

                for plt in series:
                    for y in tmp_item:
                        if y[2] == plt['name']:
                            plt['data'][index_count] = y[0] or 0
                            

            index_count += 1 

                
        # initialization 
        
        pie_chat_values = [0 for x in service_names]
        index_count = 0
        
        for item in service_name_list:

            for x in sales_dist_data:
 
                if x.label == item:
                    pie_chat_values[index_count] = x.amount
                    break

            index_count += 1


    return render_template('dashboard.html', 
                            plot_data=series,
                            
                            total_users=total_users,
                            new_users=newly_created_users,
                            
                            successful_transact=success_trans,
                            failed_transact=failed_trans,
                            amount_transact=success_trans_amount,
                            year=today.year,
                            cur_month=today.strftime('%B'),
                            service_labels=service_name_list,
                            pie_chat_values=pie_chat_values,
                            payment_info=payment_info,
                            cur_fmt=h.currency_formatter
                            )



@app.route("/logout")
@is_active_session
def logout():
    
    # perform proper logout later on 

    del session['admin_username']
    # del session['admn_userid']

    return redirect(url_for('backend.login'))



def set_login_sessions(username):
    session["admin_username"] = username






