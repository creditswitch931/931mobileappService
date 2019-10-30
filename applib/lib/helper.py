

from configobj import ConfigObj
import json
import os, base64

import string
from random import randint, choice


def get_logo():
    location = get_config("COMPANY", "path")
    
    out = ''
    with open(location, 'rb') as fl:
        out = fl.read()

    return utf_decode(ba64_encode(out))



 

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


def dump2json(value):
    return json.dumps(value)


def currency_formatter(value):
    fmt = "{:" + str(len(str(value))) + ",.2f}"
    return fmt.format(value)



class SetUri:
    """
        # default uri 
        # dialect+driver://username:password@host:port/database

        # default uri 
        # dialect+driver://username:password@host:port/database

        # postgresql uri structure 
        >>> postgresql://scott:tiger@localhost:5432/mydatabase 
        # sqlite uri structure 
        >>> sqlite:///foo.db

    """

    def __init__(self, db_cfg):
        self.db_cfg = db_cfg


    def set_credentials(self):
        tmp = self.db_cfg
        output = ''
        
        if tmp['username']:
            output = tmp['username'] + ':' + tmp["password"]

        return output


    def set_connections(self):
        
        output = ''

        if self.db_cfg['host']:
            output = '@'+ self.db_cfg['host'] + ':' + self.db_cfg['port']

        return output


    def set_db(self):        
        return  '/' + self.db_cfg['database']


    def set_driver(self):
        output = self.db_cfg['dialect'] 
        if self.db_cfg.get('driver', None):
            output += '+' + self.db_cfg['driver']

        output += '://'

        return output


    def run(self):
        
        return (self.set_driver() + self.set_credentials() 
                + self.set_connections() + self.set_db()
                )



def set_db_uri():

    _db_cfg = get_config('DB')
    uri = SetUri(_db_cfg)
    return uri.run()


def utf_encode(value):
    return value.encode('utf-8')


def utf_decode(value):
    return value.decode('utf-8')


def ba64_encode(ord_value):
    output = base64.b64encode(ord_value)
    return output


def ba64_decode(encoded_value):
    output = base64.b64decode(encoded_value)
    return output 


def save_file(img_obj, pathfolder):

    path = ''
    if img_obj:
        path = os.path.join(pathfolder, img_obj.filename)

        img_obj.save(path)

    return path 



def random_num(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    out = randint(range_start, range_end)
    return str(out)


def random_alphanum(size=6):
    #ascii_uppercase
    chars=string.ascii_lowercase + string.digits    
    return ''.join(choice(chars) for _ in range(size))


