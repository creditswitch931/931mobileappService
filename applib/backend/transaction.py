
from flask import (Blueprint, url_for, request, 
					render_template, redirect)
from applib.lib import helper  as h
from applib.backend import bk_form as fm 
from applib import model as m 
import os
import datetime
from sqlalchemy import func


from .service_config import UPLOAD_FOLDER, set_pagination

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('transaction', __name__, url_prefix='/backend')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


def date_format(date_obj, strft='%H: %M: %S'):
	
	now = datetime.datetime.now()
	diff = now - date_obj

	if diff.days == 0:
		retv = date_obj.strftime(strft)

	elif diff.days == 1:
		retv = 'Yesterday'

	elif diff.days > 1 and diff.days < 10:
		retv = date_obj.strftime('%d, %B')

	else:
		retv = date_obj.strftime("%d-%m-%Y")
	

	return retv


@app.route('/transaction/view', methods=['POST', 'GET'])
def transaction_view():
	with m.sql_cursor() as db:
		data = db.query(m.Transactions.id,
							m.Transactions.trans_ref,
							m.Transactions.trans_desc,
							m.Transactions.trans_params,
							m.Transactions.trans_resp,
							m.Transactions.date_created, 
							m.MobileUser.full_name,
							m.ServiceItems.label.label('item_name'),
							m.ServicesMd.label.label('service_name')
						).outerjoin(
								m.MobileUser,
								m.MobileUser.id == m.Transactions.user_id
						).outerjoin(
								m.ServiceItems,
								m.ServiceItems.id == m.Transactions.trans_type_id
						).join(
								m.ServicesMd,
								m.ServicesMd.id == m.ServiceItems.service_id
						).order_by(m.Transactions.id.desc()).all()

		data_count=db.query(func.count(m.Transactions.id)).scalar() 

	

		# print(data.count())
		# import pudb
		# pudb.set_trace()
	return render_template('transaction.html', data=data, data_count=data_count)

@app.route('/', methods=['POST', 'GET'])
def add():
	pass


