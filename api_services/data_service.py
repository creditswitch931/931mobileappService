import base64
import bcrypt
import requests
import json
import random
from .api_lib import get_config, hash_data
from applib.api.resp_handler import RequestHandler

public_key='j6kHi1NXAOjrHFk0'
private_key="XY1t9Y159hWJaETD"

auth_login='38457'

# auth_login='17000'
# public_key='f7a2b427dedbdbdc4825675b306741ff2772a9243b938faa7fb2db2a5615fd0b6a88b5ae33b0d21b3c60c64e7ceb2c49e1cbe73063dad713430af1abbb884662'
# private_key="c555b496d8a3c659547bb84bf1e3cae25f4cbec7f81913f3cf35abb48fa23b6eeaefe74f6489aa97d083e6dcabeccaa1a6acde6b6623a9bd5e0ff604fbf389ad"


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

    payload = {'loginId': login_id, 'authId': auth_login, 'key': public_key, 'requestId': request_id, 
                'serviceId': service_id, 'amount': amount, 'recipient' : recipient , 'checksum': checksum_data, 'ip':'54.198.95.28'} 

    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv


def data_plan(login_id, service_id):
    url = get_config('SERVICES', 'data_plan')

    payload = {'loginId': login_id, 'key': public_key, 'serviceId': service_id}

    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv

