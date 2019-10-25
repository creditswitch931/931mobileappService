
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

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@app.route('/item/add', methods=['POST', 'GET'])
def item_add():

    form = fm.ServiceItem(**request.form)
    
    if request.method == 'POST' and form.validate():

        _path = h.save_file(request.files[form.image.name], UPLOAD_FOLDER)

        with m.sql_cursor() as db:
 
            _mdl = m.ServiceItems()
            m.form2model(form, _mdl, exclude=['image'])
            _mdl.image = _path

            db.add(_mdl)
            
        return redirect(url_for('service_item.item_view'))

    form.service_id.choices = [(0, 'Select Service')] + form.service_id.choices
    return render_template('item.html', form=form)

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


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

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@app.route('/item/edit/<int:item_id>/', methods=['POST', 'GET'])
def item_edit(item_id):
    
    form = fm.ServiceItem(**request.form)

    if request.method == 'POST' and form.validate():

        _path = h.save_file(request.files[form.image.name], UPLOAD_FOLDER)

        with m.sql_cursor() as db:
            qry = db.query(m.ServiceItems).get(item_id)
            m.form2model(form, qry, exclude=['image'])
            qry.image = _path or qry.image
            
            # save to db 
            db.add(qry)

        return redirect(url_for('service_item.item_view'))

    
    form.service_id.choices = [(0, 'Select Service')] + form.service_id.choices 
    data = m.ServiceItems.get_items(item_id)
    m.model2form(data, form)
    image = "/" + "/".join(data.image.split("/")[1:])
    
    return render_template('item_edit.html', form=form, image=image)
        

          
