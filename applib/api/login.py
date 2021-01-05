
from flask import (Blueprint, url_for, request, render_template)

from .resp_handler import Response, RequestHandler, FormHandler
from applib.lib import helper  as h
from applib import forms as fm 
from applib import model as m
import datetime
import os


#STATUS CODE 0 FOR LOGIN & REGISER == CANNOT VIEW DASHBOARD YET (ACTIVATE  USER)
#STATUS CODE 1 FOR LOGIN & REGISER == VIEW DASHBOARD
#STATUS CODE 2 FOR LOGIN == COMPLETE REGISTRATION
# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('customers', __name__, url_prefix='/api')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

@app.route("/login", methods=['POST'])
def access_login():    

    content = h.request_data(request)
    print(content)
    resp = Response()
        
    form = fm.LoginForm(**content)
    fh = FormHandler(form, 
                    exclude_data=["password"],
                    exclude_field=['mac_address', 'code'])

    if not fh.is_validate():

        resp.add_params("fields", fh.render())
        resp.failed()
        resp.add_message(fh.get_errormsg())
        return resp.get_body()
    

    url = h.get_config("API", "login")
    
    # if user.active is False 
    # user needs to activate their token
    user_device = None

    with m.sql_cursor() as db:

        qry = db.query(m.MobileUser.active, m.MobileUser.id,
                       m.MobileUser.full_name,
                       m.MobileUser.email,
                       m.MobileUser.phone,
                       m.MobileUser.username
                      ).filter(m.MobileUser.username == content['username']
                               ).order_by(m.MobileUser.id).first()
        
        if qry:

            user_device = db.query(m.Devices.mac_address
                                  ).filter(m.Devices.user_id==qry.id,
                                           m.Devices.mac_address == content['mac_address'],
                                           m.Devices.active == 1
                                          ).first()

    if not qry:
        
        form.username.errors = ['Unknown username specified.']
        #resp.add_params('fields', fh.render())
        resp.add_params("status", 0)

        content['user_registered'] = 0
        # resp.failed()
        # resp.add_message("Unknown username specified")

        # return resp.get_body()


    if qry:
        if qry.active == 0 and not content.get('code'):
            form.username.errors = ['account not activated yet']
            content['user_device'] = 0
            resp.add_params("status", 0)
            #resp.add_params('fields', fh.render())

            # Proceed to API to send Email with token
            # resp.failed()

            # return resp.get_body()
 
    # how to detect another mobile activation??


    if qry:
        if not user_device and not content.get('code'):
    
            form.username.errors = ['Unregistered device detected. please activate device first']
            resp.add_params("status", 0)
            #resp.add_params('fields', fh.render())
            content['user_device'] = 0

            # Proceed to API to send Email with token

            # resp.failed()
            # resp.add_message("Unregistered device detected.")

            # return resp.get_body()


    if not user_device and content.get("code"):

        max_device_allowed = h.get_config("DeviceMgr", 'max')
        with m.sql_cursor() as db:
            total = db.query(m.Devices.id).filter_by(user_id=qry.id, active=1).count()

        if total >= int(max_device_allowed):
            resp.failed()
            resp.add_params("status", 3)
            resp.add_message("Allowed Maximum device count has been reached.")

            return resp.get_body()


    # else it will be sent for verification     

    rh = RequestHandler(url, method=1, data=content)
    retv = rh.send()
    print("Response:",retv[0])
    
    # status is 1 when the token has been validated
    resp.api_response_format(retv[1])
    
    print("Response Status:",resp.status())

    if resp.status() and retv[0] >= 200 and retv[0] < 300:
        #IF USER IS ACTIVE ON CSW BUT NOT REGISTERED ON MOBILE DATABASE
        if not qry:
            print("======Incomplete registration=======")
            #CHECK ACTIVE STATUS ON CSW
            #IF ACTIVE JUST COPY DETAILS TO MOBILE DB AND LOGIN 
             
            if retv[1].get('status') == 1 :
                active = True
                status = 1
            else :
                active = False
                status = 0
                resp.failed()
                resp.add_message("Inactive account/device! An SMS has been sent to your phone, "+ retv[1].get('phone') +" with your activation token.")

            print(active)
            print(status)

            user_id = ""

            with m.sql_cursor() as db:

                _mdl = m.MobileUser()
                _mdl.full_name = retv[1].get('name')
                _mdl.email = retv[1].get('email')
                _mdl.phone = retv[1].get('phone')
                _mdl.username = retv[1].get('phone')
                _mdl.active = active
                _mdl.date_created = datetime.datetime.now() 

                db.add(_mdl)
                db.flush()

                user_id = _mdl.id

                dev = m.Devices()
                dev.user_id = _mdl.id
                dev.mac_address = content['mac_address']
                dev.active = True
                dev.date_created = datetime.datetime.now()
                db.add(dev)
            
            resp.add_params('user_id', user_id) # get this from the mobile_usertable 
            resp.add_params("ussd_gtb", ["*737*50*", "*931#"])
            resp.add_params("ussd_all", ["*402*96609931*", "#"])        

            resp.add_params("status", status)
            resp.add_params('fields', fh.render())

            
            return resp.get_body()


        if content.get("code") is not None:
            with m.sql_cursor() as db:
                qry_resp = db.query(m.MobileUser).get(qry.id)
                qry_resp.active = True

                if not user_device:                   
                    # can always llimit the number of concurrent devices here 
                    
                    max_device_allowed = int(h.get_config("DeviceMgr", "max"))

                    # check how many devices are active 
                    total_device = db.query(m.Devices.id).filter(
                                            m.Devices.active==1, m.Devices.user_id==qry.id
                                            ).count()

                    if total_device <= max_device_allowed:

                        dev = m.Devices()
                        dev.user_id = qry.id
                        dev.mac_address = content['mac_address']
                        dev.active = True
                        dev.date_created = datetime.datetime.now()
                        db.add(dev)


        #resp.add_params('username', qry.username if os.getenv("MODE") == '1' else os.getenv('GLOBALUSERNAME'))
        #resp.add_params('username', qry.username)
        resp.add_params('fields', fh.render())
        resp.add_params("name", qry.full_name)
        resp.add_params("email", qry.email)
        resp.add_params("phone", qry.phone)
        resp.add_params('user_id', qry.id) # get this from the mobile_usertable 
        resp.add_params("ussd_gtb", ["*737*50*", "*931#"])
        resp.add_params("ussd_all", ["*402*96609931*", "#"])        

        resp.add_params("status", 1)

    elif (not resp.status()) and retv[0] >= 200 and retv[0] < 300:
        if retv[1].get('statusCode') == 'C002': # 931 merchant
            resp.remove_params("status")
            resp.add_params("status", 2)
        elif retv[1].get('statusCode') == 'C001': # inactive merchant
            resp.remove_params("status")
            resp.add_params("status", 0)
        else:
            resp.remove_params("status")
            resp.add_params("status", 4)

        resp.add_params('fields', fh.render())

    else:
        resp.add_message("Error logging, please retry")
        resp.add_params('fields', fh.render())
    
    return resp.get_body()


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@app.route("/register", methods=['POST', "GET"])
def register():
    content = h.request_data(request) or {}
    resp = Response()
    
    url = h.get_config("API", "register")

    form = fm.RegistrationForm(**content)
    fh = FormHandler(form, 
                     exclude_data=["password", "password_confirmation"],
                     exclude_field=['mac_address'])

    if request.method == 'GET':
        resp.add_params("fields", fh.render())
        resp.success()
        return resp.get_body()


    if not fh.is_validate():

        resp.add_params("fields", fh.render())
        resp.failed()
        resp.add_message(fh.get_errormsg())
        return resp.get_body()


    # form validated successfully. 

    content['full_name'] = content.pop('first_name') + ' ' + content.pop('last_name')

    rh = RequestHandler(url, method=1, data=content)
    retv = rh.send()
    print(retv)

    if retv[1]['statusCode'] == "00" or retv[1]['statusCode'] == 'C001':
        
        with m.sql_cursor() as db:
            _mdl = m.MobileUser()
            m.form2model(form, _mdl, exclude=['first_name', 'last_name', 'password', 'password_confirmation', 'mac_address'])
            _mdl.full_name = content['full_name']
            _mdl.active = False if retv[1]['statusCode'] == 'C001' else True
            _mdl.username = form.phone.data #retv[1].get('username')
            _mdl.date_created = datetime.datetime.now() 

            db.add(_mdl)
            db.flush()

            dev = m.Devices()
            dev.user_id = _mdl.id
            dev.mac_address = content['mac_address']
            dev.active = True
            dev.date_created = datetime.datetime.now()
            db.add(dev)

        if retv[1]['statusCode'] == '00': #Active account, proceed to login
            resp.remove_params("status")
            resp.add_params("status", 1)
        elif retv[1]['statusCode'] == 'C001': # Inactive account, activate
            resp.remove_params("status")
            resp.add_params("status", 0)
        
    
    resp.api_response_format(retv[1])

    return resp.get_body()


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@app.route("/forgot", methods=['POST'])
def handle_password_recovery():
    
    content = h.request_data(request)
    resp = Response()
    
    cfg = h.get_config("API")    

    url = cfg['reset_password_sms']

    rh = RequestHandler(url, method=1, data=content)
    retv = rh.send()

    resp.api_response_format(retv[1])
    return resp.get_body()


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@app.route("/update_password", methods=['POST'])
def update_password():

    content = h.request_data(request)
    resp = Response()

    url = h.get_config("API", "update_password")

    rh = RequestHandler(url, method=1, data=content)
    retv = rh.send()

    resp.api_response_format(retv[1])
    return resp.get_body()


@app.route("/add_password", methods=['POST'])
def add_password():

    content = h.request_data(request)
    resp = Response()

    url = h.get_config("API", "add_password")

    rh = RequestHandler(url, method=1, data=content)
    retv = rh.send()

    resp.api_response_format(retv[1])
    return resp.get_body()


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


def get_balance(username):

    url = h.get_config("API", "balance")    
    rh = RequestHandler(url, method=1, data={"username": username})
    retv = rh.send()
    print("retv====", retv, "\n\n")
    
    bal = retv[1].get('balance') 
    
    if bal:
        retv[1]['balance'] = h.currency_formatter(float(bal))
    
    return retv 


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@app.route("/balance", methods=['GET'])
def fetch_api_balance():
    
    params = h.request_data(request)
    retv = get_balance(params['username']) 
    
    resp = Response()
    resp.api_response_format(retv[1])        

    return resp.get_body()


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

@app.route("/resendotp")
def resend_otp():

    content = h.request_data(request)
    resp = Response()

    qry = None

    _phone = content.get('phone')
    _mac_add = content.get('mac_address')

    with m.sql_cursor() as db:
        if _phone:
            qry = db.query(m.MobileUser.phone
                      ).filter_by(phone=content.get('phone')
                                 ).first()
        elif _mac_add:
            qry = db.query(m.MobileUser.phone, m.Devices.id).join(
                    m.Devices,
                    m.Devices.user_id == m.MobileUser.id 
                ).filter(m.Devices.mac_address == _mac_add,
                         m.Devices.active == 1
                        ).first()

    if not qry:
        resp.failed()
        resp.add_message("Unknown mobile device")

        return resp.get_body()


    url = h.get_config("API", "resend_otp_code")

    rh = RequestHandler(url, method=1, data={"phone": qry.phone})
    retv = rh.send()

    resp.api_response_format(retv[1])
    return resp.get_body()


@app.route("/resendvoiceotp")
def resend_voice_otp():

    content = h.request_data(request)
    resp = Response()

    qry = None

    _phone = content.get('phone')
    _mac_add = content.get('mac_address')

    with m.sql_cursor() as db:
        if _phone:
            qry = db.query(m.MobileUser.phone
                      ).filter_by(phone=content.get('phone')
                                 ).first()
        elif _mac_add:
            qry = db.query(m.MobileUser.phone, m.Devices.id).join(
                    m.Devices,
                    m.Devices.user_id == m.MobileUser.id 
                ).filter(m.Devices.mac_address == _mac_add,
                         m.Devices.active == 1
                        ).first()

    if not qry:
        resp.failed()
        resp.add_message("Unknown mobile device")

        return resp.get_body()


    url = h.get_config("API", "resend_voice_otp")

    rh = RequestHandler(url, method=1, data={"phone": qry.phone})
    retv = rh.send()

    resp.api_response_format(retv[1])
    return resp.get_body()



# @app.route("/errors")
# def store_logs():
#     """
#     Log Tracker
#     -----------
#     """
    
#     # not yet implemented 
    
#     from sentry_sdk import capture_message

#     capture_message()

    