
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

@app.route('/mobile/users', methods=['POST', 'GET'])
@is_active_session
def users():
	content = h.request_data(request)
	with m.sql_cursor() as db:
		data = db.query(m.MobileUser.full_name,
						m.MobileUser.email,
						m.MobileUser.phone
					)
		if content.get('q') is not None:
			data = data.filter(or_(
								   m.MobileUser.full_name.like('%' + content['q'] + '%'), 
								   m.MobileUser.email.like('%' + content['q'] + '%'),
								   m.MobileUser.phone.like('%' + content['q'] + '%')
								  )
							   )

		data = data.order_by(m.MobileUser.id.desc()).all()

		data_count=db.query(func.count(m.MobileUser.id)).scalar()

	return render_template('mobile.html', data=data)
		


