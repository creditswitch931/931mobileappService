

from flask import (Blueprint, url_for, request, render_template)

from .resp_handler import Response, RequestHandler, FormHandler
from applib.lib import helper  as h
from applib import forms as fm 
from applib import model as m
from applib.api import service_handler as sh
from applib.backend.service_config import set_pagination 

import os 


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
                                m.ServiceItems.service_id == content['id']
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

    print("\n", content, '\n')
    # {'service_id': 1, 'name': 'mtn', 'item_id': 1, 
    # 'service_name': 'airtime', 'amount': '897889', 'phone': '58247'}

    # form handler instance
    fm_handler = get_form_by_name(content['form_cls'], 
                          content['fields'])
    
    HandlerCls = get_handler_cls(content['name'])
    handler_cls = HandlerCls(fm_handler.get_fields(), resp, 
                             login_id=content['user_name'],
                             name=content['name'],
                             ref_id=content['item_id'],
                             mac_address=content['mac_address'],
                             user_id=content['user_id']
                            )



    # fm_handler.readonly_field = handler_cls.__readonlyFields__

    if not fm_handler.is_validate():
        resp.failed()
        resp.add_message(fm_handler.get_errormsg())
        resp.add_params("API_forms", fm_handler.render())

        return resp.get_body()
    
    
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
    
    HandlerCls = get_handler_cls(content['name'])    
    handler_cls = HandlerCls(fm_handler.get_fields(), resp, 
                             login_id=content['user_name'],
                             name=content['name'],
                             ref_id=content['item_id'],
                             mac_address=content['mac_address'],
                             user_id=content['user_id'])

    # fm_handler.readonly_field = handler_cls.__readonlyFields__
    if not fm_handler.is_validate():
        resp.failed()
        resp.add_message(fm_handler.get_errormsg())
        resp.add_params("API_forms", fm_handler.render())
        resp.add_params('API_formCls', handler_cls.__formCls__)

        return resp.get_body()
    
    
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
    
    fields = ["page", 'page_size', 'user_id']

    for key, val in  content.items():
        if key in fields:
            _req[key] = int(val)

        else:
            _req[key] = val



    page_size = 10 
 
    with m.sql_cursor() as db:
        qry = db.query( 
            m.Transactions.id,            
            m.Transactions.trans_desc,
            m.Transactions.trans_params,
            m.Transactions.trans_resp,
            m.Transactions.trans_amount,
            m.Transactions.date_created,
            m.Transactions.trans_desc,
            m.Transactions.trans_code,
            m.ServiceItems.label,
            m.ServiceItems.image
        ).outerjoin(
            m.ServiceItems,
            m.ServiceItems.id == m.Transactions.trans_type_id

        ).filter(
            m.Transactions.user_id == _req['user_id']
        ).order_by(m.Transactions.id.desc()) 

        params, _rows = set_pagination(qry, _req["page"], _req.get('page_size') or page_size)

    
    retv = []
    # exclude = ['responseCode', "responseDesc", "login_id"]

    for x in params.items:
        
        retv.append({
            "status": x.trans_desc,
            "request": h.json_str2_dic(x.trans_params),
            "service_label": x.label,
            "trans_amount": x.trans_amount,
            "response": format_data(h.json_str2_dic(x.trans_resp)),
            "date_created": h.date_format(x.date_created),
            "image": get_base64_image(x.image),
            "responseCode": x.trans_code,
            "responseDesc": x.trans_desc
        })

    
    if retv:
        resp.success()
    
    else:
        resp.failed()

    resp.add_params('transhistory', retv)

    return resp.get_body()



def format_data(iterobj):
    
    exclude = ["login_id"]
    retv = [] 

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

 

      








