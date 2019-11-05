
from flask import (Blueprint, url_for, request, 
					render_template, redirect)
from applib.lib import helper  as h
from applib.backend import bk_form as fm 
from applib import model as m 
import os
from sqlalchemy import func

from .service_config import UPLOAD_FOLDER, set_pagination

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('mobile', __name__, url_prefix='/backend')


@app.route('/mobile/users', methods=['POST', 'GET'])
def users():
	with m.sql_cursor() as db:
		data = db.query(m.MobileUser.full_name,
						m.MobileUser.email,
						m.MobileUser.phone
					).order_by(m.MobileUser.id.desc()).all()
		
		data_count=db.query(func.count(m.MobileUser.id)).scalar()

	return render_template('mobile.html', data=data)
		


