
from flask import (Blueprint, url_for, request, 
                    render_template, redirect)
from applib.lib import helper  as h
from applib.backend import bk_form as fm 
from applib import model as m 
import os

from .service_config import UPLOAD_FOLDER, set_pagination

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('transaction', __name__, url_prefix='/backend')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

@app.route('/', methods=['POST', 'GET'])
def transact_view():
	with m.sql_cursor() as db:
		data = db.query(m.Transactions.id,
							m.Transactions.trans_ref,
							m.Transactions.trans_desc,
							m.Transactions.trans_params,
							m.Transactions.trans_resp, 
							m.MobileUser.full_name
						).outerjoin(
								m.MobileUser,
								m.MobileUser.id == m.Transactions.user_id
							).order_by(m.Transactions.id.desc()).all()
		
		
	return render_template('transaction.html', data=data)
# id trans_ref trans_desc trans_params trans_resp user_id

@app.route('/', methods=['POST', 'GET'])
def add():
	pass
