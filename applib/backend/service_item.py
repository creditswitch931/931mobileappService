
from flask import (Blueprint, url_for, request, 
					render_template, redirect)

from applib.lib import helper  as h
from applib.backend import bk_form as fm 
from applib import model as m 
import os


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('service_item', __name__, url_prefix='/backend')

UPLOAD_FOLDER = 'applib/static/media'


@app.route('/item/add', methods=['POST', 'GET'])
def item_add():
	form = fm.ServiceItem(request.form)
	form.service.choices = [(0, 'Select an Item...')]

	with m.sql_cursor() as db:
		qry = db.query(m.ServicesMd).order_by(m.ServicesMd.id.desc()).all()
		form.service.choices.extend([(g.id, g.label) for g in qry])

		if request.method == 'POST' and form.validate():

			_path = h.save_file(request.files[form.image.name], UPLOAD_FOLDER)

			params = {
				'name' : form.name.data,
				'label' : form.label.data,
				'image' : _path,
				'service_id' : form.service.data,
				'active' : form.active.data
			}

			service_item = m.ServiceItems(**params)
			db.add(service_item)
			return redirect(url_for('service_item.item_list'))

	return render_template('item.html', form=form)


@app.route('/item/list', methods=['POST', 'GET'])
def item_list():
	form = ServiceItem(request.form)
	service = { x[0]: x[1] for x in form.service.choices }
	with m.sql_cursor() as db:
		data = db.query(m.ServiceItems.id,
						m.ServiceItems.name,
						m.ServiceItems.label,
						m.ServiceItems.service_id
			  ).order_by(m.ServicesMd.id.desc()).limit(10).all()


	return render_template('item_list.html', data=data, service_label=service)



@app.route('/item/edit', methods=['POST', 'GET'])
def item_edit():
	pass
