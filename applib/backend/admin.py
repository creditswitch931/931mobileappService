
from flask import (Blueprint, url_for, request, render_template, send_from_directory)

from applib.lib import helper  as h
from applib.backend import forms as fm 
from applib import model as m 
import base64
import os
from PIL import Image
# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('admin', __name__, url_prefix='/backend')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+



@app.route('/add', methods=['POST', 'GET'])
def add():

	form = fm.Service(request.form)
	if request.method == 'POST':

		if form.service_image.data:
			image_file = request.files[form.image.name]
	
			UPLOAD_FOLDER = 'applib/media'
			_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
			image_file.save(_path)

			params = {
				'name': form.service_name.data,
				'label': form.service_label.data,
				'image': _path
			}

			with m.sql_cursor() as db:
				services = m.Services(**params)
				db.add(services)
		

	return render_template('admin.html', form=form)


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


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


@app.route('/edit/<int:service_id>/', methods=['POST', 'GET'])
def edit(service_id):
	with m.sql_cursor() as db:
		param = {'id': service_id}

		data = db.query(m.Services.name,
						m.Services.label,
						m.Services.image).filter_by(**param)
		data = data.first()

		# form = fm.Service() 
		# request.form['service_name'] = data.name
		# request.form['service_label'] = data.label
		# form.service_image.data = image.show()
		# # import pudb
		# # pudb.set_trace()
		UPLOAD_FOLDER = 'applib/media'
		# _path = data.image
		# image = Image.open(_path)

		image = send_from_directory(UPLOAD_FOLDER,
                               filename= data.image, as_attachment=True)

		if request.method == 'POST':
			image_file = request.files['service_image']
	
			UPLOAD_FOLDER = 'applib/media'
			_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
			image_file.save(_path)
			data.update(
				{
					'name': request.form['service_name'],
					'label': request.form['service_label'],
					'image': _path
				})

	return render_template('edit.html', data=data, image=image)