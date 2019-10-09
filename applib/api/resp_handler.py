
import json 

import requests as rq 


class Response:
    """ 
        Response Class  Doc
        ===================

    """
    def __init__(self, code='', desc=''):
        self.params = {"responseCode": code, 
                       'responseDesc': desc, "data": []}


    def add_params(self, key, value):
        self.params['data'].append({key, value})


    def add_message(self, message):
        self.params["responseDesc"] =  message

    def success(self):
        self.params['responseCode'] = "0"

    def failed(self):
        self.params['responseCode'] = "1"

    def get_body(self):
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





class RequestHandle:

    def __init__(self, url, method=0, data={}, headers={"content-type": "application/json"}):

        self.method = "GET" if method == 0 else "POST"
        self.url = url
        self.data = data 
        self.headers = headers 

    def send(self):

        if self.method == "POST":
            assert self.data , "Data parameter is missing for post method"

        if self.method == "GET":
            output = rq.get(self.url, headers=self.headers)
        else:
            output = rq.post(self.url, data=self.data, headers=self.headers)

        try:
            resp = output.status_code, output.json()            
        except Exception as e:
            resp = output.status_code, {} 
            # log this exception 
        
        return resp 