
from flask import (Blueprint, url_for, request, 
                    render_template, redirect)
from applib.lib import helper  as h
from applib.backend import bk_form as fm 
from applib import model as m 

from .service_config import set_pagination
import datetime
from .web_login import is_active_session

from sqlalchemy import or_
# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('service_plan', __name__, url_prefix='/backend/plan')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

@app.route("/")
@is_active_session
def index():

    with m.sql_cursor() as db:
        page = request.args.get('page', 1, type=int)
        per_page=10
        
        data = db.query(m.ServicePlan.id,
                        m.ServicePlan.code,
                        m.ServicePlan.label,
                        m.ServicePlan.group_name,
                        m.ServiceItems.label.label('service_name')
                ).join(
                    m.ServiceItems,
                    m.ServiceItems.id == m.ServicePlan.service_id
                ).order_by(m.ServicePlan.id.desc())

        content = h.request_data(request)
        if content.get('q') is not None:
            data = data.filter(or_(
                                   m.ServicePlan.code.like('%' + content['q'] + '%'), 
                                   m.ServicePlan.label.like('%' + content['q'] + '%'),
                                   m.ServicePlan.group_name.like('%' + content['q'] + '%'),
                                   m.ServiceItems.label.like('%' + content['q'] + '%')
                                  )
                               )
        data = data.order_by(m.ServicePlan.id.desc())

        pager, _rows = set_pagination(data, page, per_page)
 
    return render_template("service_plan_list.html", pager=pager, 
                            page_row=_rows, cur_page=page)


@app.route("/add", methods=['POST', 'GET'])
@is_active_session
def add():

    content = h.request_data(request)
    form = fm.ServicePlan(**content)    
    form.service_id.choices = form.service_id.choices + [(x.id, x.label) for x in m.ServiceItems.get_all()]
   

    if request.method == 'POST' and form.validate():

        mdl = m.ServicePlan()
        m.form2model(form, mdl)
        mdl.date_created = datetime.datetime.now()

        with m.sql_cursor() as db:
            db.add(mdl)

        return redirect(url_for('service_plan.index'))


    return render_template("service_plan_form.html", form=form, _title='Add Plan', 
                           back_url='service_plan.index')


@app.route('/edit/<int:id>', methods=['POST', 'GET'])
@is_active_session
def edit(id):

    content = h.request_data(request)
    form = fm.ServicePlan(**content)    
    form.service_id.choices = form.service_id.choices + [(x.id, x.label) for x in m.ServiceItems.get_all()]

    if request.method == 'POST':

        with m.sql_cursor() as db:
            obj = db.query(m.ServicePlan).get(id)
            m.form2model(form, obj)
            db.add(obj)

        return redirect(url_for('service_plan.index'))

    data = m.ServicePlan.get_items(id)
    m.model2form(data, form, exclude=['date_created'])


    return render_template('service_plan_form.html', form=form, 
                           _title='Edit Plan', back_url='service_plan.index')



