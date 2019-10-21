
import os 
import importlib

from flask import Flask, redirect, render_template 
from flask_cors import CORS


# +---------------------------+---------------------------+
# 
# +---------------------------+---------------------------+

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})



# +---------------------------+---------------------------+
# Sub Module Registraton
# +---------------------------+---------------------------+

def module_register(_foldername='api'):

    root_folder = app.root_path.split('/')[-1]
    app_path = os.path.join(root_folder, _foldername)
    
    if 'docs' in os.getcwd():
        return 
    for mod in os.listdir(app_path):
        if mod.endswith('.py'):
            mod = mod.split('.py')[0]
            _path  = os.path.join(app_path, mod)
            
            dotted_path = '.'.join(_path.split('/'))            
            _mod = importlib.import_module(dotted_path)

            if hasattr(_mod, 'app'):
                app.register_blueprint(_mod.app)



module_register()
module_register("backend")


