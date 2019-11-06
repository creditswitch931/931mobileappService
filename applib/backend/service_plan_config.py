
from flask import (Blueprint, url_for, request, 
                    render_template, redirect)
from applib.lib import helper  as h
from applib.backend import bk_form as fm 
from applib import model as m 

from .service_config import set_pagination

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('service_plan', __name__, url_prefix='/backend/plan')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

@app.route("/")
def index():

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
                ).order_by(m.ServiceItems.id.desc())

        pager, _rows = set_pagination(data, page, per_page)

    return render_template("service_plan_list.html", pager=[], page_row=_rows)



@app.route("/add")
def add():

    return "WIP"