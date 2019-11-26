
from flask import (Blueprint, url_for, request, 
                    render_template, redirect)
from applib.lib import helper  as h
from applib.backend import bk_form as fm 
from applib import model as m 
import os

from sqlalchemy import func, or_

from .service_config import UPLOAD_FOLDER, set_pagination
from .web_login import is_active_session

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('mobile', __name__, url_prefix='/backend')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

@app.route('/mobile/users')  # , methods=['POST', 'GET'])
@is_active_session
def users():

    content = h.request_data(request)
    page = int(content.get('page')) if content.get('page') else 1
    per_page = 10

    with m.sql_cursor() as db:
        data = db.query(m.MobileUser.full_name,
                        m.MobileUser.email,
                        m.MobileUser.phone,
                        m.Devices.mac_address
                    ).outerjoin(
                        
                        m.Devices, 
                        m.Devices.user_id == m.MobileUser.id
                    ).filter(
                        m.Devices.active == 1
                    ).order_by(
                        m.MobileUser.id.desc()
                    )
        if content.get('q') is not None:
            data = data.filter(or_(
                                   m.MobileUser.full_name.like('%' + content['q'] + '%'), 
                                   m.MobileUser.email.like('%' + content['q'] + '%'),
                                   m.MobileUser.phone.like('%' + content['q'] + '%')
                                  )
                               )

        
        
        data, page_rows = set_pagination(data, page, per_page)


    return render_template('mobile.html', data=data,
                            page_row=page_rows, cur_page=content.get('page'))
        


