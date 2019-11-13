
from flask import (Blueprint, url_for, request, 
					render_template, redirect)

from sqlalchemy_pagination import paginate
from applib.lib import helper  as h
from applib.backend import bk_form as fm 
from applib import model as m 
import os
from .web_login import is_active_session
from sqlalchemy import or_
# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('bk_cfg', __name__, url_prefix='/backend')

UPLOAD_FOLDER = 'applib/static/media'


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@app.route('/service/add', methods=['POST', 'GET'])
@is_active_session
def add():

	form = fm.Service(**request.form)
	
	if request.method == 'POST' and form.validate():

		_path = h.save_file(request.files[form.image.name], UPLOAD_FOLDER)
 
		with m.sql_cursor() as db:

			_mdl = m.ServicesMd()
			m.form2model(form, _mdl, exclude=['image'])
			_mdl.image = _path

			db.add(_mdl)

			return redirect(url_for("bk_cfg.service_view"))
		

	return render_template('service.html', form=form)


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@app.route('/service/view', methods=['POST', 'GET'])
@is_active_session
def service_view():
	
	content = h.request_data(request)

	with m.sql_cursor() as db:
		page = request.args.get('page', 1, type=int)
		per_page=10
		data = db.query(m.ServicesMd.id,
						m.ServicesMd.name,
						m.ServicesMd.label,
						m.ServicesMd.category_name
			  			)

		if content.get('q') is not None:
			data = data.filter(or_(
                                   m.ServicesMd.name.like('%' + content['q'] + '%'), 
                                   m.ServicesMd.label.like('%' + content['q'] + '%'),
                                   m.ServicesMd.category_name.like('%' + content['q'] + '%')
                                  )
							  )

		data = data.order_by(m.ServicesMd.id.desc())
		

		users, page_row = set_pagination(data, page, per_page)
		

	return render_template('service_list.html', data=data, users=users, 
							page_row=page_row, cur_page=page)


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+



@app.route('/service/edit/<int:service_id>/', methods=['POST', 'GET'])
@is_active_session
def edit(service_id): 
		 
	form = fm.Service(**request.form)

	if request.method == 'POST' and form.validate():
		 
		_path = h.save_file(request.files[form.image.name], UPLOAD_FOLDER)

		with m.sql_cursor() as db:
			qry = db.query(m.ServicesMd).get(service_id)
			m.form2model(form, qry, exclude=['image'])
			qry.image = _path or qry.image
			
			db.add(qry)
		return redirect(url_for("bk_cfg.service_view"))

	with m.sql_cursor() as db:
		data = db.query(m.ServicesMd).filter_by(id=service_id).first()
		m.model2form(data, form)
		form.active.data = data.active == 1
		
		image = "/" + "/".join(data.image.split("/")[1:])

	return render_template('service_edit.html', form=form, data=data, image=image)



@app.route('/service/delete/<int:service_id>')
@is_active_session
def delete(service_id):

	with m.sql_cursor() as db:
		param = {'id': service_id}
	   
		db.query(m.ServicesMd).filter_by(**param).delete()

		return redirect(url_for('bk_cfg.service_view')) 
 


def set_pagination(obj, cur_page, page_size):
	
	pager = paginate(obj, cur_page, page_size)
 
	start_no = cur_page - 1 
	if start_no < 1:
		start_no = cur_page

	counter = 0
	page_lists = []

	for x in range(start_no, pager.pages + 1 ):
		page_lists.append(x)
		counter += 1 
		if counter > 7:
			break


	return  pager, page_lists


