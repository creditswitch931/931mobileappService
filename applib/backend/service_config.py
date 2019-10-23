
from flask import (Blueprint, url_for, request, 
                    render_template, redirect)

from applib.lib import helper  as h
from applib.backend import bk_form as fm 
from applib import model as m 
import os


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('bk_cfg', __name__, url_prefix='/backend')

UPLOAD_FOLDER = 'applib/static/media'


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+



@app.route('/add', methods=['POST', 'GET'])
def add():

    form = fm.Service(**request.form)

    if request.method == 'POST':

        image_file = request.files['service_image']
         
        if image_file:
                
            _path = os.path.join(UPLOAD_FOLDER, image_file.filename)
            image_file.save(_path)

            params = {
                'name': form.service_name.data,
                'label': form.service_label.data,
                'image': _path,
                'category_name': form.category_name.data
            }

            with m.sql_cursor() as db:
                services = m.ServicesMd(**params)
                db.add(services)


            return redirect(url_for("bk_cfg.service_view"))
        

    return render_template('admin.html', form=form)


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@app.route('/service/list', methods=['POST', 'GET'])
def service_view():
    with m.sql_cursor() as db:
        data = db.query(m.ServicesMd.id,
                        m.ServicesMd.name,
                        m.ServicesMd.label,
                        m.ServicesMd.category_name
              ).order_by(m.ServicesMd.id.desc()).limit(10).all()


    return render_template('list.html', data=data)


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@app.route('/edit/<int:service_id>/', methods=['POST', 'GET'])
def edit(service_id): 
         
    form = fm.Service(**request.form)

    if request.method == 'POST' and form.validate():

        image_file = request.files['service_image']
                    
        _path = os.path.join(UPLOAD_FOLDER, image_file.filename)
        image_file.save(_path)

        with m.sql_cursor() as db:
            qry = db.query(m.ServicesMd).get(service_id)
            qry.name = form.service_name.data 
            qry.label = form.service_label.data
            qry.category_name = form.category_name.data
            qry.image = _path

            db.add(qry)

        return redirect(url_for("bk_cfg.service_view"))


    with m.sql_cursor() as db:
        param = {'id': service_id}

        data = db.query(m.ServicesMd.name,
                        m.ServicesMd.label,
                        m.ServicesMd.image,
                        m.ServicesMd.category_name).filter_by(**param).first()

        # temporary fix, to be cleaned up later 

        form.service_name.data = data.name 
        form.service_label.data = data.label
        form.category_name.data = data.category_name 
 

        image = "/" + "/".join(data.image.split("/")[1:])
       



    return render_template('edit.html', form=form, data=data, image=image)