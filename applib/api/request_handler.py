

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
