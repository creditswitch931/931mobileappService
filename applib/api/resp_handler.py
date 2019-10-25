
import json 

import requests as rq 
import urllib

class Response:
    """ 
        Response Class  Doc
        ===================

    """
    def __init__(self, code='', desc=''):
        self.params = {"responseCode": code, 
                       'responseDesc': desc, "data": []}


    def add_params(self, key, value):
        self.params['data'].append({key: value})


    def add_message(self, message):
        self.params["responseDesc"] =  message

    def success(self):
        self.params['responseCode'] = "0"

    def failed(self):
        self.params['responseCode'] = "1"

    def get_body(self):
        print('API Response', self.params, '\n\n')
        return json.dumps(self.params)

    def api_response_format(self, obj_resp):

        # {'statusCode': '00',
        #  'statusDescription': 'Login Successful',
        #  'mac_address': '02:00:00:44:55:66',
        #  'transaction_ref': '$2y$10$aAMtVP5QGeXt1vNMJwipO.hkwRGle.UrUk3L8Y14aHJ3336Tnd5X.'}

        for key, value in obj_resp.items():

            if key == "statusCode":
                if value == "00":
                    self.success()
                else: 
                    self.failed()

                continue

            if key == "statusDescription":
                self.add_message(value)
                continue


            self.add_params(key, value)





class RequestHandler:

    def __init__(self, url, method=0, data={}, headers={"content-type": "application/json"}):

        self.method = "GET" if method == 0 else "POST"
        self.url = url
        self.data = data 
        self.headers = headers 

    def send(self):

        if self.method == "POST":
            assert self.data , "Data parameter is missing for post method"

        print("=== Request Data ===", self.data, '\n\n')
        if self.method == "GET":
            self.format_get_params()
            output = rq.get(self.url, headers=self.headers)
        else:
            output = rq.post(self.url, data=json.dumps(self.data), 
                             headers=self.headers)

        try:
            resp = output.status_code, output.json()            
        except Exception as e:
            resp = output.status_code, {} 
            # log this exception 
        
        return resp 

    def format_get_params(self):
        if self.data:
            self.url = self.url + "?" + urllib.parse.urlencode(self.data)



class FormHandler:

    def __init__(self, form, exclude_data=[], exclude_field=[]):
        self.form = form
        self.fields = []
        self.exclude_data = exclude_data
        self.exclude_field = exclude_field

    def render(self):

        prev = None
        total = len(self.form._fields) - len(self.exclude_field)
        count = 1
        field_names = []
        
        for x in self.form:
            if x.name in self.exclude_field:
                continue

            field_names.append(x.name)


        for field, obj in self.form._fields.items():
            if field in self.exclude_field:
                continue

            _f = {
                "name" : obj.label.text,
                "field": field,
                "value": obj.data if field not in self.exclude_data else None,
                "retkey" : "next" if count < total else "done" ,
                "error" : obj.errors[0] if obj.errors else None,
                "nextfield" : field_names[count] if count < total else None,
                "type": self.set_type(obj.type),
                "encrypt": True  if obj.type == 'PasswordField' else False
            }

            self.fields.append(_f)
            count += 1 

        return self.fields


    def set_type(self, _type):

        if _type =='IntegerField':
            return 'numeric'
        
        return 'default'


    def get_errormsg(self):       

        for fld, obj in self.form.errors.items():
            return "field {} {}".format(fld, obj[0])


    def is_validate(self):        
        return self.form.validate()


