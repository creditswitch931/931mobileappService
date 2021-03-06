import base64
import bcrypt
import requests
import json
import random
from .api_lib import get_config, hash_data
from applib.api.resp_handler import RequestHandler
 
#auth_login='38457'
#public_key='j6kHi1NXAOjrHFk0'
#private_key="XY1t9Y159hWJaETD"

auth_login='269545'
public_key='VZAYfjcn44DJUzE2k25MHK4h6LAOMwLZo5dRApNKd1M7UI3SC8woCaMgcHaOL3YrKdEPOg0VaC3TDdlVDxlIm8eZ57'
private_key="XPdmWNq9n1TitNhcPTQpCMg6J2TbikCBVX39aKaW4PVPShJ7Epo9K83ut3aF4dbVe9zvB9aM3jiHdrC5C0huxdcGCV"

def airtime_vending(login_id, amount, recipient, provider, 
                        request_id):

    # request_id = random.randrange(10000000, 99999999)
    # request_id = str(request_id)

    if provider == "airtel":
        service_id = "A01E"
    elif provider == "9mobile":
        service_id = "A02E"
    elif provider == "globacom":
        service_id = "A03E"
    elif provider == "mtn":
        service_id = "A04E" 


    checksum = (str(login_id) + "|" + request_id + "|" + service_id + "|" + str(amount) + "|" +
                private_key + "|" + recipient)

    checksum_data = hash_data(checksum)

    url = get_config('SERVICES', 'airtime')

    #payload = {'loginId': login_id, 'key': public_key, 'requestId': request_id, 'serviceId': service_id, 
    #            'amount': amount, 'recipient' : recipient , 'checksum': checksum_data} 

    payload = {'loginId': login_id, 'authId': auth_login, 'key': public_key, 'requestId': request_id, 'serviceId': service_id, 'amount': amount, 'recipient' : recipient , 'checksum': checksum_data, 'ip':'54.198.95.28'} 

    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv


# deprecated and will be removed 
# def send_sms(login_id, public_key, private_key, sender_id, msisdn, message_body):
#     transaction_ref = ''.join(random.choice('0123456789ABCDEF') for i in range(16))

#     checksum = str(login_id) + "|" + private_key + "|" + transaction_ref
#     checksum_data = hash_data(checksum)

#     send_sms = get_config('SERVICES')
#     request_url = send_sms['sms']

#     payload = {'loginId': login_id, 'key': public_key, 'senderId': sender_id, 
#                 'msisdn': msisdn, 'messageBody': message_body, 
#                 'transactionRef': transaction_ref, 'checksum': checksum_data}

#     rh = RequestHandler(url, method=1, data=payload)
#     retv = rh.send()
#     return retv

