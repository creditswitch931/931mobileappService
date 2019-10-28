

from flask import (Blueprint, url_for, request, render_template)

from .resp_handler import Response, RequestHandler, FormHandler
from applib.lib import helper  as h
from applib import forms as fm 
from applib import model as m
from applib.api import service_handler as sh

FORMS = {
    'airtime': ''
}

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('request', __name__, url_prefix='/api')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

def get_base64_image(img_path):

    output = ""
    _type = img_path.split('/')[-1]
    _type = _type.split('.')[-1]

    schema = "data:image/png;base64,"

    if _type.lower() == 'jpg':
        schema = "data:image/jpg;base64,"

    
    with open(img_path, 'rb') as fl:
        output = h.utf_decode(h.ba64_encode(fl.read()))
        

    return schema + output

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

def get_form_objects(entity):

    entity_cls = getattr(sh, entity.title() +'Handler')        
    form_cls = getattr(fm, entity_cls.__formCls__)
    form_ins = FormHandler(form_cls())
    


    return form_ins.render(), entity_cls.__url__, entity_cls.__form_label__

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

@app.route("/get/services")
def get_services():

    content = h.request_data(request)
    resp = Response()

    """
        service  object 
            name
            label
            image/ icon in base64  

    """

    retv = []

    with m.sql_cursor() as db:
        qry = db.query(
            m.ServicesMd.id,
            m.ServicesMd.name,
            m.ServicesMd.label,
            m.ServicesMd.image,
            m.ServicesMd.category_name
        ).filter(m.ServicesMd.active == True)
 
        
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
                       ).filter(m.ServiceItems.active == True,
                                m.ServiceItems.service_id == content['id']
                       ).all()


        for item in qry:
            form_info = get_form_objects(item.service_name)

            retv.append({"name": item.name, 
                         "label": item.label,
                         "item_id": item.id,
                         "label_desc": item.label_desc,
                         "service_name": item.service_name,
                         "image": get_base64_image(item.image),
                         "forms": form_info[0],
                         "url_path": form_info[1],
                         "btn_label": form_info[2]
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


    resp.success()
    resp.add_message("Transaction successfull")
    resp.add_params("transaction_id", 10)
    return resp.get_body()




@app.route("/service/validate", methods=['POST'])
def process_validation():
    
    content = h.request_data(request)

    # form_object
    # {'meter_number': '09900', 'amount': '9890-0-', 'phone': 'Eefj', 
    # 'service_id': 2, 'name': 'ibadan_distro', 'item_id': 6, 
    # 'service_name': 'Electricity'} 

    print("\n", content, '\n')

    resp = Response()

    resp.success()
    resp.add_message("Validation successfull")
    resp.add_params("transaction_id", 10)

    return resp.get_body()






