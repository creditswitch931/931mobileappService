
from flask import (Blueprint, url_for, request, render_template)

from .resp_handler import Response, RequestHandler
from applib.lib import helper  as h


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
    
    url = h.get_config("API", "login")

    rh = RequestHandler(url, method=1, data=content)
    retv = rh.send()



    resp.api_response_format(retv[1])        
    resp.add_params("menu", [])
    resp.add_params("transactions", [])
    resp.add_params("balance", [])
    
    return resp.get_body()


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@app.route("/register", methods=['POST'])
def register():
    content = h.request_data(request)
    resp = Response()
    
    url = h.get_config("API", "register")

    rh = RequestHandler(url, method=1, data=content)
    retv = rh.send()

    resp.api_response_format(retv[1])        
    
    return resp.get_body()

    


# {
#     "statusCode": "00",
#     "statusDescription": "Registration Successful",
#     "mac_address": "1292999277",
#     "transaction_ref": "$2y$10$O0XIV8TX7VxAFQjDAhMGO.yhD5b1q..Ub.xSuHcXnDjqQJNIpooqC"
# }

# {
# "full_name":"Mr Gonzalo higuain","email":"g.higuain@yahoo.com","mac_address":"1292999277",
# "password":"password","password_confirmation":"password","phone":"0708934525"
# }



@app.route("/errors")
def store_logs():
    """
    Log Tracker
    -----------
    """
    
    from sentry_sdk import capture_message

    capture_message()

    


