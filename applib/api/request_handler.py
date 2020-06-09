

from flask import (Blueprint, url_for, request, render_template)

from .resp_handler import Response, RequestHandler, FormHandler
from applib.lib import helper  as h
from applib import forms as fm 
from applib import model as m
from applib.api import service_handler as sh
from applib.backend.service_config import set_pagination 

import os, calendar


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('request', __name__, url_prefix='/api')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

def get_base64_image(img_path):

    # repurpose this to load from a text file  so as to save processing power.

    output = ""
    _type = img_path.split('/')[-1]
    _type = _type.split('.')[-1]

    schema = "data:image/png;base64,"

    if _type.lower() == 'jpg':
        schema = "data:image/jpg;base64,"
    
    if not os.path.exists(img_path+'.txt'):
        with open(img_path, 'rb') as fl:
            output = h.utf_decode(h.ba64_encode(fl.read()))
        

        with open(img_path+".txt", "w") as fl:
            fl.write(output)

    else:
        with open(img_path+".txt", 'r') as fl:
            output = fl.read()


    return schema + output

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+


def get_handler_cls(entity):
    _cls = getattr(sh, entity + 'Handler')
    return _cls

def initialize_form(formname, fields={}):
    _Form = getattr(fm, formname)
    _form = _Form(**fields)
    _form.init_func()
    return FormHandler(_form)


def get_form(entity, fields):
    entity_cls = get_handler_cls(entity)     
    return initialize_form(entity_cls.__formCls__, fields)  

    # form_cls = getattr(fm, entity_cls.__formCls__)    
    # return FormHandler(form_cls(**fields)) 

def get_validate_form(entity, fields):

    entity_cls = get_handler_cls(entity)
    return initialize_form(entity_cls.__formClsValidate__, fields)

    # form_cls = getattr(fm, entity_cls.__formClsValidate__)
    # return FormHandler(form_cls(**fields))


def get_form_by_name(formname, fields):
    
    return initialize_form(formname, fields)

    # form_cls = getattr(fm, formname)
    # return FormHandler(form_cls(**fields))


def get_form_objects(entity, fields={}):

    entity_cls = get_handler_cls(entity)
    form_ins = initialize_form(entity_cls.__formCls__, fields)
    
    # form_cls = getattr(fm, entity_cls.__formCls__)
    # form_ins = FormHandler(form_cls(**fields))
    
    return (form_ins.render(), 
            entity_cls.__url__, 
            entity_cls.__form_label__,
            entity_cls.__formCls__)


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+
@app.route("/get/service/categories")
def get_service_categories():
    """
        Get all subcategories
    """
    content = h.request_data(request)
    resp = Response()
    retv = []
    filterquery = ""
  
    with m.sql_cursor() as db:
        if content:
            qry = db.query(m.ServiceItems.id,
                       m.ServiceItems.name,
                       m.ServiceItems.label,
                       m.ServiceItems.image,
                       m.ServiceItems.label_desc,
                       m.ServiceItems.service_id).filter(m.ServiceItems.active==1, m.ServiceItems.service_id == content['id']).all()
        else:
            qry = db.query(m.ServiceItems.id,
                       m.ServiceItems.name,
                       m.ServiceItems.label,
                       m.ServiceItems.image,
                       m.ServiceItems.label_desc,
                       m.ServiceItems.service_id).filter(m.ServiceItems.active==1).all()
        
        

        for item in qry:
            retv.append({"name": item.name, 
                         "label": item.label,
                         "item_id": item.id,
                         "label_desc": item.label_desc,
                         "service_id": item.service_id
                        }
                )

    resp.add_params('service_categories', retv)

    if retv:
        resp.success()
        resp.add_message("data fetched successfully")
    
    else:
        resp.failed()
        resp.add_message("No matching data found...")

    return resp.get_body()



@app.route("/get/services")
def get_services():

    content = h.request_data(request)
    resp = Response()

    retv = []

    with m.sql_cursor() as db:
        qry = db.query(
            m.ServicesMd.id,
            m.ServicesMd.name,
            m.ServicesMd.label,
            m.ServicesMd.image,
            m.ServicesMd.category_name
        ).filter(m.ServicesMd.active==1)
 
        
        if content.get('name'):
            qry = qry.filter(
                    m.ServicesMd.name.ilike(content.get('name'))
                )       

        for x in qry.all():
            tmp_img = get_base64_image(x.image)
            retv.append({"name": x.name, 
                         "label": x.label, 
                         "service_id": x.id,
                         "category_name":x.category_name, 
                         "image":tmp_img}
                        )

    resp.add_params("services", retv)
    
    if retv:
        resp.success()
        resp.add_message("fetched data successfully")

    else:
        resp.failed()
        resp.add_message("no service data found")


    return resp.get_body()


# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

@app.route("/get/service/items")
def get_service_items():
    
    """
        Set the form data required for the individual options

        .filter(m.ServiceItems.active==1,
            m.ServiceItems.id == content['id']
        ).
    """

    content = h.request_data(request)
    resp = Response()
    retv = []

    with m.sql_cursor() as db:
        qry = db.query(
                       m.ServiceItems.id,
                       m.ServiceItems.name,
                       m.ServiceItems.label,
                       m.ServiceItems.image,
                       m.ServiceItems.label_desc,
                       m.ServicesMd.label.label("service_label"),
                       m.ServicesMd.name.label("service_name")
                       ).join(
                        m.ServicesMd,
                        m.ServicesMd.id == m.ServiceItems.service_id
                       ).filter(m.ServiceItems.active==1,
                                m.ServiceItems.id == content['id']
                       ).all()


        for item in qry:
            form_info = get_form_objects(item.name)

            retv.append({"name": item.name, 
                         "label": item.label,
                         "item_id": item.id,
                         "label_desc": item.label_desc,
                         "service_name": item.service_name,
                         "image": get_base64_image(item.image),
                         "forms": form_info[0],
                         "url_path": form_info[1],
                         "btn_label": form_info[2],
                         "formCls": form_info[3]
                        }
                )

    resp.add_params('service_items', retv)

    if retv:
        resp.success()
        resp.add_message("data fetched successfully")
    
    else:
        resp.failed()
        resp.add_message("No matching data found...")

    return resp.get_body()



@app.route("/service/vending", methods=['POST'])
def process_service():
    
    content = h.request_data(request)
    resp = Response()

    # form handler instance
    fm_handler = get_form_by_name(content['form_cls'], 
                          content['fields'])
    
    
    
    if not fm_handler.is_validate():
        resp.failed()
        resp.add_message(fm_handler.get_errormsg())
        resp.add_params("API_forms", fm_handler.render())

        return resp.get_body()
    
    
    HandlerCls = get_handler_cls(content['name'])
    handler_cls = HandlerCls(fm_handler.get_fields(), resp, 
                             login_id=content['user_name'],
                             name=content['name'],
                             ref_id=content['item_id'],
                             mac_address=content['mac_address'],
                             user_id=content['user_id']
                            )
    
    handler_cls.vend_service()

    resp.mode(False)


    if not resp.status():
        resp.add_params("API_forms", fm_handler.render())
        resp.add_params("API_formCls", content['form_cls'])

    elif resp.status(): 
        resp.add_params('API_printout', handler_cls.get_printout())
        resp.add_params("API_details", handler_cls.get_response())
        

    return resp.get_body()




@app.route("/service/validate", methods=['POST'])
def process_validation():
    
    content = h.request_data(request)

    # form_object
    # {'fields': {'meter_number': '9090909', 
    # 'amount': '7867678989', 'phone': '7878989090'},
    # 'service_id': 2, 'name': 'ibadan_distro', 
    # 'item_id': 6, 'service_name': 'Electricity', form_cls: ""}

    
    resp = Response()

    fm_handler = get_form_by_name(content['form_cls'], 
                                  content['fields'])
        
    if not fm_handler.is_validate():
        print("Thid not validate")
        print(content)
        resp.failed()
        resp.add_message(fm_handler.get_errormsg())
        resp.add_params("API_forms", fm_handler.render())
        resp.add_params('API_formCls', content['form_cls'])

        return resp.get_body()
    
    HandlerCls = get_handler_cls(content['name'])    
    handler_cls = HandlerCls(fm_handler.get_fields(), resp, 
                             login_id=content['user_name'],
                             name=content['name'],
                             ref_id=content['item_id'],
                             mac_address=content['mac_address'],
                             user_id=content['user_id'])

    handler_cls.validate_service()    

    # lets see if this will suffice, might

    resp.mode(True)

    if not resp.status():        
        resp.add_params('API_forms', fm_handler.render())
        resp.add_params('API_formCls', handler_cls.__formCls__)
    
    return resp.get_body()


@app.route("/transaction/history")
def get_transactions():

    content = h.request_data(request)
    _req = {}

    resp = Response() 

    url = h.get_config("API", "transactions")
    
    fields = ["page", 'page_size', 'user_id']

    for key, val in  content.items():
        if key in fields:
            _req[key] = int(val)

        else:
            _req[key] = val


    rh = RequestHandler(url, method=1, data=_req)
    retv = []
    sendr = rh.send()

    if sendr[1]['statusCode'] == "00":
        print(sendr[1]['transactions'])
        retv = sendr[1]['transactions']
        resp.success()
    
    else:
        resp.failed()

    resp.add_params('transhistory', retv)

    return resp.get_body()

    # print(_req, "\n\n")
    # page_size = 10 
    
 
    # with m.sql_cursor() as db:
    #     qry = db.query( 
    #         m.Transactions.id,            
    #         m.Transactions.trans_desc,
    #         m.Transactions.trans_params,
    #         m.Transactions.trans_resp,
    #         m.Transactions.trans_amount,
    #         m.Transactions.date_created,
    #         m.Transactions.trans_desc,
    #         m.Transactions.trans_code,
    #         m.ServiceItems.label,
    #         m.ServiceItems.image,
    #         m.Transactions.trans_type_id
    #     ).outerjoin(
    #         m.ServiceItems,
    #         m.ServiceItems.id == m.Transactions.trans_type_id
    #     ).filter(
    #         m.Transactions.user_id == _req['user_id'],
    #         # m.Transactions.trans_type_id != None
    #     ).order_by(m.Transactions.id.desc()) 

    #     params, _rows = set_pagination(qry, _req["page"] or 1, _req.get('page_size') or page_size)

    
    # retv = []
    # # exclude = ['restponseCode', "responseDesc", "login_id"]

    # for x in params.items:
        
    #     retv.append({
    #         "status": x.trans_desc,
    #         "request": h.json_str2_dic(x.trans_params),
    #         "service_label": x.label if x.trans_type_id else 'Wallet Funding',
    #         "trans_amount": x.trans_amount,
    #         "response": format_data(h.json_str2_dic(x.trans_resp)),
    #         "date_created": h.date_format(x.date_created),
    #         "date_group": h.date_group(x.date_created),
    #         "day_month": h.day_month_format(x.date_created),
    #         #"image": get_base64_image(x.image) if x.trans_type_id else get_base64_image('applib/static/media/walletImage.png'),
    #         "responseCode": x.trans_code,
    #         "responseDesc": x.trans_desc,
    #         "type": "service" if x.trans_type_id else "payment"
    #     })


@app.route("/funding/history")
def get_funding_history():

    content = h.request_data(request)
    _req = {}

    resp = Response() 

    url = h.get_config("API", "funding_history")
    
    fields = ['page_size', 'user_id']

    for key, val in  content.items():
        if key in fields:
            _req[key] = int(val)

        else:
            _req[key] = val


    rh = RequestHandler(url, method=1, data=_req)
    retv = []
    sendr = rh.send()

    if sendr[1]['statusCode'] == "00":
        print(sendr[1]['funding'])
        retv = sendr[1]['funding']
        resp.success()
    
    else:
        resp.failed()

    resp.add_params('funding', retv)

    return resp.get_body()



def format_data(iterobj):
    
    exclude = ["login_id"]
    retv = [] 

    if "data" not in iterobj:
        return retv


    for item in iterobj['data']:

        for key, val in item.items(): 
            if key in exclude:
                continue

            if key == 'detail':
                print(key)


            if isinstance(val, dict): # first level check 
                
                for x , y in val.items():
                    if x in exclude:
                        continue

                    if isinstance(y, dict):  # second level check 
                        
                        for k, v in y.items():
                            if k in exclude:
                                continue

                            retv.append((k, v))

                        continue

                    retv.append((x, y))

                continue

            retv.append((key, val))

    return retv 

 

@app.route("/initiatePayment", methods=['POST'])
def payment_init():

    content = h.request_data(request)
    resp = Response()

    url = h.get_config("SERVICES", "validatepayment")

    rh = RequestHandler(url, method=1, data=content)
    retv = rh.send()   

    resp.api_response_format(retv[1])
    
    return resp.get_body()


@app.route("/authPayment", methods=['POST'])
def payment_auth():

    content = h.request_data(request)
    resp = Response()

    url = h.get_config("SERVICES", "authpayment")

    param = {
        'card_no': content['cardno'][:5] + "****" + content['cardno'][-4:],
        "amount": content['amount'], 
        "redirect_url": content['redirect_url']
    }
    trans_details = {
        "trans_ref": content['transaction_id'],
        "trans_desc": None,
        "trans_code": None,
        "trans_params": h.dump2json(param),
        "trans_resp": '[]',
        "user_mac_address": content['macaddress'],
        "user_id": content.pop("user_id"),
        "trans_type_id": None,
        "trans_amount": content['amount']
    }

    rh = RequestHandler(url, method=1, data=content)
    retv = rh.send()

    m.Transactions.save(**trans_details)

    resp.api_response_format(retv[1])
    
    # add the trasaction in a table 
    # create the record here 

    return resp.get_body()




@app.route("/processPayment", methods=['POST'])
def payment_process():

    content = h.request_data(request)
    resp = Response()


    url = h.get_config("SERVICES", "processpayment")
    
    trans_id = content.pop("transaction_id")


    rh = RequestHandler(url, method=1, data=content)
    retv = rh.send()
    
    resp.api_response_format(retv[1])
    
    # update the payment transaction record here
    content.pop('otp')
    content.update(**resp.params)

    with m.sql_cursor() as db:
        db.query(m.Transactions
                ).filter_by(trans_ref=trans_id
                ).update({"trans_desc": resp.params['responseDesc'], 
                          "trans_code":resp.params['responseCode'],
                          "trans_resp": h.dump2json(content)
                        }
                    )


    return resp.get_body()




@app.route("/get/transaction/dist")
def get_trans_distro():

    _req = {}
    
    resp = Response()

    url = h.get_config("API", "tranxstats")
    
    _req['user_id'] = h.request_data(request).get("user_id")

    print(_req, "\n\n")

    rh = RequestHandler(url, method=1, data=_req)
    retv = []
    sendr = rh.send()

    print(sendr)

    if sendr[1]['statusCode'] == "00":
        print(sendr[1]['tranxstats'])
        retv = sendr[1]['tranxstats']
        resp.success()
    
    else:
        resp.failed()

    resp.add_params('piedata', retv)

    return resp.get_body()

    # user_id = h.request_data(request).get("user_id")
        
    # _now = m.datetime.datetime.now()        
    # last_day = calendar.monthrange(_now.year, _now.month)
     
    # start_date = m.datetime.date(_now.year, _now.month, 1)
    # end_date = m.datetime.date(_now.year, _now.month, last_day[1])
    
    # output = []
    
    # color_bank = ["#2CA4E0", "#9FE02B", "#65E6F8", "#27AE60"]

    # with m.sql_cursor() as db:

    #     qry = db.query(            
    #         (m.func.count(m.Transactions.id)).label("count"),
    #         m.func.sum(m.Transactions.trans_amount.cast(m.Integer)).label('sumtotal'),
    #         m.ServiceItems.service_id,
    #         m.ServicesMd.label            
    #     ).join(
    #         m.ServiceItems,
    #         m.ServiceItems.id == m.Transactions.trans_type_id
    #     ).join(
    #         m.ServicesMd, m.ServicesMd.id == m.ServiceItems.service_id
    #     ).filter(            
    #         m.Transactions.date_created.between(start_date, end_date),
    #         m.Transactions.trans_code == '0'
    #     ).group_by(
    #         m.ServiceItems.service_id,
    #         m.ServicesMd.label 
    #     ).order_by(
    #         m.Transactions.date_created
    #     )

    #     if user_id:
    #         qry = qry.filter(
    #                 m.Transactions.user_id == user_id
    #             )

 
    #     retv = []
    #     cnt = 0
    #     total_colors = len(color_bank)

    #     for x in qry.all():
    #         retv.append(
    #             {
    #                 'value': x.count,
    #                 "name": x.label ,
    #                 "sumtotal": str(x.sumtotal),
    #                 "color" : color_bank[cnt]
    #             }
    #         )                    

    #         cnt += 1 

    #         if cnt >= total_colors:
    #             cnt = 0 # reverse the counter avoid failure 


    # if retv:
    #     resp.success()
        
    # else:
    #     resp.failed()

    
    # resp.add_params('piedata', retv)

    # return resp.get_body()


@app.route("/get/transaction/today")
def get_trans_stats_today():
    
    _req = {}
    resp = Response()

    url = h.get_config("API", "todaystats")
    
    _req['user_id'] = h.request_data(request).get("user_id")

    print(_req, "\n\n")

    # content = h.request_data(request)

    
    # fields = ['user_id']

    # for key, val in  content.items():
    #     if key in fields:
    #         _req[key] = int(val)
    #     else:
    #         _req[key] = val


    rh = RequestHandler(url, method=1, data=_req)
    retv = []
    sendr = rh.send()

    print(sendr)

    if sendr[1]['statusCode'] == "00":
        print(sendr[1]['todaystats'])
        retv = sendr[1]['todaystats']
        resp.success()
    
    else:
        resp.failed()

    resp.add_params('todaystats', retv)

    return resp.get_body()

        
    # _now = m.datetime.datetime.now()
     
    # start_date = m.datetime.date.today()
    # end_date = _now
    
    # output = []
    

    # with m.sql_cursor() as db:

    #     qry = db.query(            
    #         (m.func.count(m.Transactions.id)).label("count"),
    #         m.func.sum(m.Transactions.trans_amount.cast(m.Integer)).label('sumtotal'),
    #     ).filter(            
    #         m.Transactions.date_created.between(start_date, end_date),
    #         m.Transactions.trans_code == '0'
    #     )

    #     if user_id:
    #         qry = qry.filter(
    #                 m.Transactions.user_id == user_id
    #             )

 
    #     retv = []

    #     for x in qry.all():
    #         retv.append(
    #             {
    #                 'value': x.count,
    #                 "sumtotal": str(x.sumtotal)
    #             }
    #         )                  

    # if retv:
    #     resp.success()
        
    # else:
    #     resp.failed()

    
    # resp.add_params('todaystats', retv)

    # return resp.get_body()




@app.route("/get/transaction/stats")
def get_trans_stats():  
    
    user_id = h.request_data(request).get("user_id")
    resp = Response()

    _now = m.datetime.datetime.now()
    last_day = calendar.monthrange(_now.year, _now.month)
    
    if _now.month >  6 and _now.month <=12:
        start_month = 7

    elif _now.month >= 1 and _now.month < 7:
        start_month = 1 


    start_date = m.datetime.date(_now.year, start_month, 1)
    end_date = m.datetime.date(_now.year, _now.month, last_day[1])


    if start_month == 1:
        month_range = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        month_str_range = ["{}{}".format(_now.year, x) for x in ["01","02","03","04","05","06"]]
    else:
        month_range = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month_str_range = ["{}{}".format(_now.year, x) for x in ["07","08","09","10","11","12"]]


    with m.sql_cursor() as db:

        qry = db.query(            
            m.func.sum(m.Transactions.trans_amount.cast(m.Integer)).label('sumtotal'),
            m.func.max(m.ServiceItems.service_id),
            m.func.extract('YEAR_MONTH', m.Transactions.date_created).label("date_range")           
        ).join(
            m.ServiceItems,
            m.ServiceItems.id == m.Transactions.trans_type_id
        ).filter(
            m.Transactions.date_created.between(start_date, end_date), 
            m.Transactions.trans_code == '0',
            m.Transactions.trans_type_id != None
        ).group_by(
            m.func.extract('YEAR_MONTH', m.Transactions.date_created)
        ).order_by(
            m.func.extract('YEAR_MONTH', m.Transactions.date_created).asc()
        )


        if user_id:
            qry = qry.filter(
                    m.Transactions.user_id == user_id
                )

        retv = {'data': [], 'label': month_range}
        tmp = {}


        for x in qry.all():
            tmp[str(x.date_range)] = str(x.sumtotal)
        


        for x in month_str_range:
            if x not in tmp:
                retv['data'].append(0)
            else:
                retv['data'].append(tmp[x])            
    
    if retv['data']:
        resp.success()

    else:
        resp.failed()

    resp.add_params("linedata", retv)

    return resp.get_body()










