
from flask import (Blueprint, url_for, request, 
                    render_template, redirect)
from applib.lib import helper  as h
from applib.backend import bk_form as fm 
from applib import model as m 
import os

from .service_config import UPLOAD_FOLDER, set_pagination
from .web_login import is_active_session
from sqlalchemy import or_
# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('service_item', __name__, url_prefix='/backend')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@app.route('/item/add', methods=['POST', 'GET'])
@is_active_session
def item_add():

    form = fm.ServiceItem(**request.form)
    form.service_id.choices = form.service_id.choices + m.ServicesMd.get_service()

    if request.method == 'POST' and form.validate():

        _path = h.save_file(request.files[form.image.name], UPLOAD_FOLDER)

        with m.sql_cursor() as db:
 
            _mdl = m.ServiceItems()
            m.form2model(form, _mdl, exclude=['image'])
            _mdl.image = _path

            db.add(_mdl)
            
        return redirect(url_for('service_item.item_view'))

    

    return render_template('item.html', form=form, 
                            _title='Add Item', back_url="service_item.item_view")

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@app.route('/item/view')
@is_active_session
def item_view():
    content = h.request_data(request)
    with m.sql_cursor() as db:
        page = request.args.get('page', 1, type=int)
        per_page=10
        
        data = db.query(m.ServiceItems.id,
                        m.ServiceItems.name,
                        m.ServiceItems.label,
                        m.ServicesMd.label.label('service_name')
                ).join(
                    m.ServicesMd,
                    m.ServicesMd.id == m.ServiceItems.service_id
                )
        
        if content.get('q') is not None:
            data = data.filter(or_(
                                   m.ServiceItems.name.like('%' + content['q'] + '%'), 
                                   m.ServiceItems.label.like('%' + content['q'] + '%'),
                                   m.ServicesMd.label.like('%' + content['q'] + '%')
                                  )
                               )
        data = data.order_by(m.ServiceItems.service_id.desc())
        users, page_row = set_pagination(data, page, per_page)


    return render_template('item_list.html', data=data, users=users, 
                            page_row=page_row, cur_page=page)

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@app.route('/item/edit/<int:item_id>/', methods=['POST', 'GET'])
@is_active_session
def item_edit(item_id):
    
    form = fm.ServiceItem(**request.form)
    form.service_id.choices = form.service_id.choices + m.ServicesMd.get_service()

    if request.method == 'POST' and form.validate():

        _path = h.save_file(request.files[form.image.name], UPLOAD_FOLDER)

        with m.sql_cursor() as db:
            qry = db.query(m.ServiceItems).get(item_id)
            m.form2model(form, qry, exclude=['image'])
            qry.image = _path or qry.image
            
            # save to db 
            db.add(qry)

        return redirect(url_for('service_item.item_view'))

    
    data = m.ServiceItems.get_items(item_id)
    m.model2form(data, form)
    form.active.data = data.active == 1 
    image = "/" + "/".join(data.image.split("/")[1:])
    
    return render_template('item.html', form=form, image=image,  
                            _title='Edit Item', back_url="service_item.item_view")
        


@app.route('/item/delete/<int:item_id>')
@is_active_session
def delete(item_id):

    with m.sql_cursor() as db:
        param = {'id': item_id}
       
        db.query(m.ServiceItems).filter_by(**param).delete()

        return redirect(url_for('service_item.item_view')) 
          
