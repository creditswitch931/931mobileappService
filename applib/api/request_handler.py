

from flask import (Blueprint, url_for, request, render_template)

from .resp_handler import Response, RequestHandler, FormHandler
from applib.lib import helper  as h
from applib import forms as fm 
from applib import model as m



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
        {
            name : item_name,
            label: item label,
            img : display            
        }
    """

    content = h.request_data(request)
    resp = Response()
    retv = []

    print('\n\n', content, '\n\n')

    with m.sql_cursor() as db:
        qry = db.query(m.ServiceItems.name,
                m.ServiceItems.label,
                m.ServiceItems.image,
                m.ServicesMd.label.label("service_label"),
                m.ServicesMd.name.label("service_name")
            ).join(
                m.ServicesMd,
                m.ServicesMd.name == content['name']
            ).filter(m.ServicesMd.active == True,
                     m.ServiceItems.active == True
                    ).all()

        for item in qry:
            retv.append({"name": item.name, "label": item.label,
                         "service_name": content['name'],
                         "image": h.get_base64_image(item.image)
                        }
                )

    if retv:
        resp.success()
        resp.add_message("data fetched successfully")
        resp.add_params('service_items', retv)

    else:
        resp.failed()
        resp.add_message("No matching data found...")

    return resp.get_body()


