
from flask import (Blueprint, url_for, request, 
                    render_template, redirect)

from applib.lib import helper  as h
from applib.backend import bk_form as fm 
from applib import model as m 
import os

from .service_config import UPLOAD_FOLDER 

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('service_item', __name__, url_prefix='/backend')

# UPLOAD_FOLDER = 'applib/static/media'


@app.route('/item/add', methods=['POST', 'GET'])
def item_add():

    form = fm.ServiceItem(**request.form)
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
			
			return redirect(url_for('service_item.item_view'))

        print(form.errors)

    return render_template('item.html', form=form)


@app.route('/item/list', methods=['POST', 'GET'])
def item_view():
	form = fm.ServiceItem(**request.form)

    with m.sql_cursor() as db:
        
        data = db.query(m.ServiceItems.id,
                        m.ServiceItems.name,
                        m.ServiceItems.label,
                        m.ServicesMd.label.label('service_name')
                ).join(
                    m.ServicesMd,
                    m.ServicesMd.id == m.ServiceItems.service_id
                ).order_by(
                    m.ServiceItems.id.desc()
                ).limit(10).all()


    return render_template('item_list.html', data=data)



@app.route('/item/edit/<int:item_id>/', methods=['POST', 'GET'])
def item_edit(item_id):
	form = fm.ServiceItem(**request.form)

	with m.sql_cursor() as db:
		
		param = {'id': item_id}

		data = db.query(m.ServiceItems.name,
						m.ServiceItems.label,
						m.ServiceItems.image,
						m.ServiceItems.service_id,
						m.ServiceItems.active,
						m.ServicesMd.label.label('service_name')
						).join(
							m.ServicesMd,
							m.ServicesMd.id == m.ServiceItems.service_id
							).filter(m.ServiceItems.id == item_id).first()


		form.service.choices = [(0, 'Select a service...')]
		qry = db.query(m.ServicesMd).order_by(m.ServicesMd.id.desc()).all()
		form.service.choices.extend([(g.id, g.label) for g in qry])

		form.name.data = data.name
		form.label.data = data.label
		form.active.data = data.active
		form.service.data = data.service_id

		image = "/" + "/".join(data.image.split("/")[1:])

		if request.method == 'POST' and form.validate():

			_path = h.save_file(request.files[form.image.name], UPLOAD_FOLDER)

			qry = db.query(m.ServiceItems).get(item_id)
			qry.name = form.name.data
			qry.label = form.label.data
			qry.image = _path or qry.image
			qry.service_id = form.service.data
			qry.active = form.active.data

			db.add(qry)

			return redirect(url_for('service_item.item_view'))

	return render_template('item_edit.html', form=form, image=image)
		

		  

 