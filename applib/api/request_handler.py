

from flask import (Blueprint, url_for, request, render_template)

from .resp_handler import Response, RequestHandler, FormHandler
from applib.lib import helper  as h
from applib import forms as fm 

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('request', __name__, url_prefix='/api')

@app.route("/get/services")
def get_services():


    content = h.request_data(request)
    resp = Response()

    if content.get('name'):

    	pass

    	# filter by given name 

    
