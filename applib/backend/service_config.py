
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


@app.route('/service/add', methods=['POST', 'GET'])
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


@app.route('/service/list', methods=['POST', 'GET'])
def service_view():
    with m.sql_cursor() as db:
        data = db.query(m.ServicesMd.id,
                        m.ServicesMd.name,
                        m.ServicesMd.label,
                        m.ServicesMd.category_name
              ).order_by(m.ServicesMd.id.desc()).limit(10).all()


    return render_template('service_list.html', data=data)


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@app.route('/service/edit/<int:service_id>/', methods=['POST', 'GET'])
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


    data = m.ServicesMd.get_items(service_id)
    m.model2form(data, form)
    image = "/" + "/".join(data.image.split("/")[1:])

    return render_template('service_edit.html', form=form, data=data, image=image)

