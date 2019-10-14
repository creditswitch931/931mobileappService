

from configobj import ConfigObj
import json


def get_config(header, key=None, filename='settings.cfg'):

    cfg = ConfigObj(filename)
    if not key:
        return cfg[header]

    return cfg[header][key]


def request_data(request):
    """
        Request Data Function 
        ---------------------
        Function to get data coming to the application for all methods.

    """

    if request.method == 'GET':
        return request.args

    elif request.method == 'POST':
        if request.data:
            return unloadJson(request.data) 

        return request.form
    
    return []


def switch_loggers(log_msg=' '):

	from sentry_sdk import capture_message
	
	cfg = get_config("SENTRY")
	if cfg.get("enabled") == '0':
		capture_message(log_msg)

	else:
		log_handler(log_msg) # call the log handler 



def log_handler(log_msg=''):
	
	# application logger function 
	# :return logger_obj:  this returns an object that will trap exceptions to a file.
	# if the log_msg contains data, it will log to the logger_objs file specified. 
	pass


def unloadJson(value):
    return json.loads(value.decode('utf-8'))






