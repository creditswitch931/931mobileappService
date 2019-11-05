
from flask import (Blueprint, url_for, request, render_template)

from .resp_handler import Response, RequestHandler, FormHandler
from applib.lib import helper  as h
from applib import forms as fm 
from applib import model as m

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('customers', __name__, url_prefix='/api')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

@app.route("/login", methods=['POST'])
def access_login():
    """
    Login Function
    ==============

    Function to handle login and authentication for the clients. 
    the below information describes the request and response data for this view.
    
    Request Data:
        Url pathname and http method to access this function
        
        :param url: ``http://BASEURL/api/login``.
        
        :param method: ``POST``
                
        Request Body::

            {
                username: client username (str) -- <phone, email, username/>,
                passwd:  client password
            }  
        

    Response Data:        
        Response data type is json.

        On failed authentication.
            Response Body::

                {
                    responseCode: 1,
                    responseDesc: invalid credentials. either user name or password is incorrect.
                }
        

        On success authentication.
            Response body::

                {
                    responseCode: 0,
                    responseDesc: User login successful,
                    data: [
                        {"Last 5 Transaction": [...]},
                        {"CurrentBalance": 891029},
                        {"Menu": [...]},
                        {"FormObject": [Airtime Form object]}
                    ]

                }
    """    

    content = h.request_data(request)
    resp = Response()
    
    form = fm.LoginForm(**content)

    if not form.validate():

        fh = FormHandler(form, 
                        exclude_data=["password"],
                        exclude_field=['mac_address'])

        resp.add_params("fields", fh.render())
        resp.failed()
        resp.add_message(fh.get_errormsg())
        return resp.get_body()
    
    url = h.get_config("API", "login")
    
    rh = RequestHandler(url, method=1, data=content)
    retv = rh.send()

    resp.api_response_format(retv[1])        
    resp.add_params("menu", [])
    resp.add_params('programs', [])
    resp.add_params("name", "Jerrey Uzodinma Alpha")
    resp.add_params('user_id', 3) # get this from the mobile_usertable 

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

    if retv[1]['statusCode'] == "00":
        
        with m.sql_cursor() as db:
            _mdl = m.MobileUser()
            m.form2model(form, _mdl, exclude=['first_name', 'last_name', 'password', 'password_confirmation'])
            _mdl.full_name = content['full_name']
            _mdl.active = True
            db.add(_mdl)

    resp.api_response_format(retv[1])
 
    return resp.get_body()


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@app.route("/forgot", methods=['POST'])
def handle_password_recovery():
    
    content = h.request_data(request)
    resp = Response()
    
    cfg = h.get_config("API")    

    form = fm.ForgotForm(**content)

    if not form.validate():
        fh = FormHandler(form)

        resp.add_params("fields", fh.render())
        resp.failed()
        resp.add_message(fh.get_errormsg())
        return resp.get_body()


    if "@" in content['email']: 
        url = cfg['reset_password_email']
        _data = {'email': content['email']}

    else:
        url = cfg['reset_password_sms']
        _data = {"phone": content['email']}


    rh = RequestHandler(url, method=1, data=_data)
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


@app.route("/errors")
def store_logs():
    """
    Log Tracker
    -----------
    """
    
    # not yet implemented 
    
    from sentry_sdk import capture_message

    capture_message()

    


