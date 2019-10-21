
from flask import (Blueprint, url_for, request, render_template)

from .resp_handler import Response, RequestHandler, FormHandler
from applib.lib import helper  as h
from applib import forms as fm 
from applib import model as m 
import requests
import json
# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('service', __name__, url_prefix='/api')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+



@app.route('/service', methods=['POST', 'GET'])
def service():
	
	with m.sql_cursor() as db:
		data = db.query(m.Services.id,
					   	m.Services.name,
					   	m.Services.label).all()
		data = json.dumps(data)

		
		resp = Response()
		resp.api_response_format(reqv[1])
		resp.get_body()
# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

