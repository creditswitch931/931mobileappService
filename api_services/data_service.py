import base64
import bcrypt
import requests
import json
import random
from .api_lib import get_config, hash_data
from applib.api.resp_handler import RequestHandler

public_key='j6kHi1NXAOjrHFk0'
private_key="XY1t9Y159hWJaETD"


def data_vending(login_id, amount, recipient, provider, request_id):
    
    request_id = str(request_id)

    if provider == "airtel":
        service_id = "D01D"
    elif provider == "9mobile":
        service_id = "D02D"
    elif provider == "globacom":
        service_id = "D03D"
    elif provider == "mtn":
        service_id = "D04D" 

    checksum = (str(login_id) + "|" + request_id + "|" + 
                service_id + "|" + str(amount) + "|" +
                private_key + "|" + recipient)

    checksum_data = hash_data(checksum)

    url = get_config('SERVICES', 'airtime')

    payload = {'loginId': login_id, 'key': public_key, 'requestId': request_id, 
                'serviceId': service_id, 'amount': amount, 
                'recipient' : recipient , 'checksum': checksum_data} 

    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv


def data_plan(login_id, service_id):
    url = get_config('SERVICES', 'data_plan')

    payload = {'loginId': login_id, 'key': public_key, 'serviceId': service_id}

    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv

