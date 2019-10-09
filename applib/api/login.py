
from flask import (Blueprint, url_for, request, render_template)

from .resp_handler import Response, RequestHandle
from applib.lib import helper  as h


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('customers', __name__, url_prefix='/api')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

@app.route("/login", methods=['POST', 'GET'])
def access_login():
    """
    Login Function
    ==============

    Functon to handle login and authentication for the clients. 
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

    rh = RequestHandle(url, method=1, data=content)
    retv = rh.send()

    resp.api_response_format(retv[1])        
    resp.add_param("menu", [])
    resp.add_param("transactions", [])
    resp.add_param("balance", [])
    
    return resp.get_body()


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

@app.route("/errors")
def store_logs():
    """
    Log Tracker
    -----------
    """
    
    from sentry_sdk import capture_message

    capture_message()

    


