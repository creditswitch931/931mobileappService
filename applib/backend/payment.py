
from flask import (Blueprint, url_for, request, 
                    render_template, redirect)
from applib.lib import helper  as h
from applib.backend import bk_form as fm 
from applib import model as m 
import os

from .service_config import UPLOAD_FOLDER, set_pagination
from .web_login import is_active_session

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

app = Blueprint('payment', __name__, url_prefix='/backend')

# +-------------------------+-------------------------+
# +-------------------------+-------------------------+

@app.route('/', methods=['POST', 'GET'])
@is_active_session
def payment_view():
	pass