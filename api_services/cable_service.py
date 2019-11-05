import base64
import bcrypt
import requests
import json
import random
from .api_lib import get_config, hash_data
from applib.api.resp_handler import RequestHandler


public_key='j6kHi1NXAOjrHFk0'
private_key="XY1t9Y159hWJaETD"


def startimes_validate(login_id, smart_card_code):
    checksum = str(login_id) + "|" + private_key + "|" + str(smart_card_code)
    checksum_data = hash_data(checksum)

    url = get_config('SERVICES', 'star_validate')

    payload = {'loginId': login_id, 'key': public_key, 'smartCardCode': smart_card_code, 
                'checksum': checksum_data}

    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv


def startimes_vending(login_id, smart_card_code, amount, transaction_ref):
    
    # transaction_ref = ''.join(random.choice('0123456789ABCDEF') for i in range(16))

    checksum = str(login_id) + "|" + private_key + "|" + str(smart_card_code) + "|" + str(amount)
    checksum_data = hash_data(checksum)

    url = get_config('SERVICES', 'star_recharge')

    payload = {'loginId': login_id, 'key': public_key, 
                'smartCardCode': smart_card_code, 
                'fee': amount, 'transactionRef': transaction_ref, 
                'checksum': checksum_data}

    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv


def multichoice_validate(login_id, customer_no, service_id):
    checksum = str(login_id) + "|" + private_key + "|" + str(customer_no)
    checksum_data = hash_data(checksum)

    url = get_config('SERVICES', 'multi_validate')

    payload = {'loginId': login_id, 'key': public_key, 'customerNo': customer_no, 
                'serviceId': service_id, 'checksum': checksum_data}

    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv



def multichoice_fetch_product(login_id, service_id):
    url = get_config('SERVICES', 'multi_fetch_prod')

    payload = {'loginId': login_id, 'key': public_key, 'serviceId': service_id}

    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv



def multichoice_fetch_product_addons(login_id, service_id):
    url = get_config('SERVICES', 'multi_fetch_prod')

    payload = {'loginId': login_id, 'key': public_key, 'serviceId': service_id}

    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv



def multichoice_vending(login_id, customer_no, customer_name, 
                        service_id, amount, invoice_period, 
                        productCodes, transaction_ref):

    # transaction_ref = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
    
    checksum = (str(login_id) + "|" + private_key + "|" 
                + customer_no + "|" + transaction_ref + "|" + str(amount))
    
    checksum_data = hash_data(checksum)

    url = get_config('SERVICES', 'multi_recharge')

    payload = {'loginId': login_id, 'key': public_key, 'serviceId': service_id, 
                'checksum': checksum_data, 'transactionRef': transaction_ref, 
                'customerNo': customer_no, 'customerName': customer_name, 
                'productCodes': productCodes, 'amount': amount, 
                'invoicePeriod': invoice_period}

    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv



