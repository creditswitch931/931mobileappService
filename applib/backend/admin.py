
from flask import (Blueprint, url_for, request, render_template)

from applib.lib import helper  as h
from applib import forms as fm 
from applib import model as m 
import base64


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('admin', __name__, url_prefix='/backend')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+



@app.route('/add', methods=['POST', 'GET'])
def add():

	if request.method == 'POST':

		image_file = request.files['service_image']
		
		encoded_string = base64.b64encode(image_file.read())
		image_file = encoded_string.decode('utf-8')

		params = {
			'name': request.form['service_name'],
			'label': request.form['service_label'],
			'image': image_file
		}

		with m.sql_cursor() as db:
			services = m.Services(**params)
			db.add(services)
		

	return render_template('admin.html')



@app.route('/list', methods=['POST', 'GET'])
def list():
	with m.sql_cursor() as db:
		data = db.query(m.Services.id,
					   	m.Services.name,
					   	m.Services.label
			  ).order_by(m.Services.id.desc()).limit(10).all()

	return render_template('list.html', data=data)



# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

