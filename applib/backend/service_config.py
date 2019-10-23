
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

    if request.method == 'POST' and form.validate():

        _path = h.save_file(request.files[form.image.name], UPLOAD_FOLDER)
 
        params = {
            'name': form.name.data,
            'label': form.label.data,
            'image': _path,
            'category_name': form.category_name.data,
            'active': form.active.data
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

    if request.method == 'POST':
         
        _path = h.save_file(request.files[form.image.name], UPLOAD_FOLDER)

        # _path = os.path.join(UPLOAD_FOLDER, image_file.filename)
        # image_file.save(_path)

        with m.sql_cursor() as db:
            qry = db.query(m.ServicesMd).get(service_id)
            qry.name = form.name.data 
            qry.label = form.label.data
            qry.image = _path or qry.image 
            qry.category_name = form.category_name.data
            qry.active = form.active.data 

            db.add(qry)

        return redirect(url_for("bk_cfg.service_view"))


    with m.sql_cursor() as db:
        param = {'id': service_id}

        data = db.query(m.ServicesMd.name,
                        m.ServicesMd.label,
                        m.ServicesMd.image,
                        m.ServicesMd.category_name,
                        m.ServicesMd.active
                        ).filter_by(**param).first()

        # temporary fix, to be cleaned up later 

        form.name.data = data.name 
        form.label.data = data.label
        form.active.data = data.active
        form.category_name.data = data.category_name

        image = "/" + "/".join(data.image.split("/")[1:])

    return render_template('edit.html', form=form, data=data, image=image)

