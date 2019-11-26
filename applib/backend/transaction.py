
from flask import (Blueprint, url_for, request, 
					render_template, redirect)
from applib.lib import helper  as h
from applib.backend import bk_form as fm 
from applib import model as m 
import os
import datetime
from sqlalchemy import func

from .service_config import UPLOAD_FOLDER, set_pagination
from .web_login import is_active_session 

from sqlalchemy import or_



# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('transaction', __name__, url_prefix='/backend')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


@app.route('/transaction/view')
@is_active_session
def transaction_view():

	content = h.request_data(request)
	page = request.args.get('page', 1, type=int)
	per_page=10

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
						).outerjoin(
								m.ServicesMd,
								m.ServicesMd.id == m.ServiceItems.service_id
						).filter(
							m.Transactions.trans_type_id != None
						)

		if content.get('q') is not None:
			data = data.filter(or_(
								   m.ServiceItems.label.like('%' + content['q'] + '%'), 
								   m.ServicesMd.label.like('%' + content['q'] + '%'),
								   m.Transactions.trans_params.like('%' + content['q'] + '%')
								  )
							   )
		data = data.order_by(m.Transactions.id.desc())

		data, page_rows = set_pagination(data, page, per_page)
		


	return render_template('transaction.html', page_data=data, 
						   page_row=page_rows, cur_page=page, 
						   date_fmt=h.date_format, get_field=get_ref_field)



def get_ref_field(fieldname, data):

	obj = h.json_str2_dic(data)
	return obj.get(fieldname) or 'N/A'



@app.route('/payment/view')
@is_active_session
def payment_view():

	content = h.request_data(request)
	page = request.args.get('page', 1, type=int)
	per_page=10

	with m.sql_cursor() as db:
		data = db.query(m.Transactions.id,
						m.Transactions.trans_ref,
						m.Transactions.trans_desc,
						m.Transactions.trans_params,
						m.Transactions.trans_resp,
						m.Transactions.date_created, 
						m.MobileUser.full_name						
						).outerjoin(
								m.MobileUser,
								m.MobileUser.id == m.Transactions.user_id
						).filter(
							m.Transactions.trans_type_id == None
						)

		data = data.order_by(m.Transactions.id.desc())

		data, page_rows = set_pagination(data, page, per_page)
	

	return render_template('payment.html', page_data=data, 
						   page_row=page_rows, cur_page=page, 
						   date_fmt=h.date_format, get_field=get_ref_field)






