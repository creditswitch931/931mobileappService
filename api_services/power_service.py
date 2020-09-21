import base64
import bcrypt
import requests
import json
import random
from .api_lib import get_config, hash_data
from applib.api.resp_handler import RequestHandler

#public_key='j6kHi1NXAOjrHFk0'
#private_key="XY1t9Y159hWJaETD"
ip = '54.198.95.28'
#auth_login='38457'

auth_login='269545'
public_key='VZAYfjcn44DJUzE2k25MHK4h6LAOMwLZo5dRApNKd1M7UI3SC8woCaMgcHaOL3YrKdEPOg0VaC3TDdlVDxlIm8eZ57'
private_key="XPdmWNq9n1TitNhcPTQpCMg6J2TbikCBVX39aKaW4PVPShJ7Epo9K83ut3aF4dbVe9zvB9aM3jiHdrC5C0huxdcGCV"



def electricity_validate(login_id, customer_account_id, service_id):

    checksum = str(login_id) + "|" + service_id + "|" + private_key + "|" + str(customer_account_id)
    checksum_data = hash_data(checksum)

    url = get_config('SERVICES', 'electic_validate')

    payload = {'loginId': login_id, 'authId': auth_login, 'key': public_key, 
               'customerAccountId': customer_account_id, 
               'serviceId': service_id, 'checksum': checksum_data,
               'ip':ip}

    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv



def electricity_vending(login_id, customer_account_id, service_id, 
                            amount, request_id):
    # request_id = random.randrange(10000000, 99999999)
    checksum = (str(login_id) + "|" + service_id + "|" + 
                private_key + "|" + str(customer_account_id) + "|" 
                + str(request_id) + "|" + str(amount)
                )

    checksum_data = hash_data(checksum)

    url = get_config('SERVICES', 'electic_recharge')

    # providerRef: to be generated from the validation response

    payload = {'loginId': login_id, 'authId': auth_login, 'key': public_key, 
               'customerAccountId': customer_account_id, 
               'serviceId': service_id, 'amount': amount, 
               'requestId': request_id, 'providerRef':'150144078049', 
               'checksum': checksum_data, 'ip':ip}

    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv 




def ikeja_prepaid(login_id, customer_account_id, service_id, 
                  amount, request_id, customerDtNumber, providerRef):

    checksum = str(login_id) + "|" + service_id + "|" + private_key + "|" + str(customer_account_id) + "|" + str(request_id) + "|" + str(amount)
    checksum_data = hash_data(checksum)

    url = get_config('SERVICES', 'electic_recharge')

    payload = {'loginId': login_id, 'authId': auth_login, 'key': public_key, 'customerAccountId': customer_account_id, 
                'serviceId': service_id, 'amount': amount, 'requestId': request_id, 
                'checksum': checksum_data, 'providerRef':providerRef, 
                'customerDtNumber':customerDtNumber, 'ip':ip}
            
    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv



def eko_prepaid(login_id, customer_account_id, service_id, 
                amount, request_id, customerDtNumber, providerRef):
    

    checksum = str(login_id) + "|" + service_id + "|" + private_key + "|" + str(customer_account_id) + "|" + str(request_id) + "|" + str(amount)
    checksum_data = hash_data(checksum)

    electricity_vending = get_config('SERVICES', 'electic_recharge')

    payload = {'loginId': login_id, 'authId': auth_login, 'key': public_key, 'customerAccountId': customer_account_id, 
                'serviceId': service_id, 'amount': amount, 'requestId': request_id, 
                'checksum': checksum_data, 'providerRef': providerRef,
                'customerDtNumber': customerDtNumber, 'ip':ip}

    # providerRef: to be generated from the validation response
     
    rh = RequestHandler(electricity_vending, method=1, data=payload)
    retv = rh.send()
    return retv


 
def ibadan_prepaid(login_id, customer_account_id, service_id, 
                   amount, request_id, customerDtNumber, providerRef):
    
    # request_id = random.randrange(10000000, 99999999)

    checksum = (str(login_id) + "|" + service_id + "|" 
                + private_key + "|" + str(customer_account_id) + "|" 
                + str(request_id) + "|" + str(amount)
               )

    checksum_data = hash_data(checksum)

    url = get_config('SERVICES', 'electic_recharge')

    payload = {'loginId': login_id, 'authId': auth_login, 'key': public_key, 
                'customerAccountId': customer_account_id, 
                'serviceId': service_id, 'amount': amount, 
                'requestId': request_id, 
                'checksum': checksum_data, 
                'providerRef': providerRef, 'thirdPartyCode': 'AKRN', 
                'customerDtNumber': customerDtNumber, 'ip':ip}

    # thirdPartyCode and providerRef: to be generated from the validation response
            
    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv

def abuja_prepaid(login_id, customer_account_id, service_id, 
                   amount, request_id, customerDtNumber, providerRef):
    
    # request_id = random.randrange(10000000, 99999999)

    checksum = (str(login_id) + "|" + service_id + "|" 
                + private_key + "|" + str(customer_account_id) + "|" 
                + str(request_id) + "|" + str(amount)
               )

    checksum_data = hash_data(checksum)

    url = get_config('SERVICES', 'electic_recharge')

    payload = {'loginId': login_id, 'authId': auth_login, 'key': public_key, 
                'customerAccountId': customer_account_id, 
                'serviceId': service_id, 'amount': amount, 
                'requestId': request_id, 
                'checksum': checksum_data, 
                'providerRef': providerRef, 'thirdPartyCode': 'AKRN', 
                'customerDtNumber': customerDtNumber, 'ip':ip}

    # thirdPartyCode and providerRef: to be generated from the validation response
            
    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv


def enugu_prepaid(login_id, customer_account_id, service_id, 
                   amount, request_id, customerDtNumber, providerRef):
    
    # request_id = random.randrange(10000000, 99999999)

    checksum = (str(login_id) + "|" + service_id + "|" 
                + private_key + "|" + str(customer_account_id) + "|" 
                + str(request_id) + "|" + str(amount)
               )

    checksum_data = hash_data(checksum)

    url = get_config('SERVICES', 'electic_recharge')

    payload = {'loginId': login_id, 'authId': auth_login, 'key': public_key, 
                'customerAccountId': customer_account_id, 
                'serviceId': service_id, 'amount': amount, 
                'requestId': request_id, 
                'checksum': checksum_data, 
                'providerRef': providerRef, 'thirdPartyCode': 'AKRN', 
                'customerDtNumber': customerDtNumber, 'ip':ip}

    # thirdPartyCode and providerRef: to be generated from the validation response
            
    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv

def portharcourt_prepaid(login_id, customer_account_id, service_id, 
                   amount, request_id, customerDtNumber, providerRef):
    
    # request_id = random.randrange(10000000, 99999999)

    checksum = (str(login_id) + "|" + service_id + "|" 
                + private_key + "|" + str(customer_account_id) + "|" 
                + str(request_id) + "|" + str(amount)
               )

    checksum_data = hash_data(checksum)

    url = get_config('SERVICES', 'electic_recharge')

    payload = {'loginId': login_id, 'authId': auth_login, 'key': public_key, 
                'customerAccountId': customer_account_id, 
                'serviceId': service_id, 'amount': amount, 
                'requestId': request_id, 
                'checksum': checksum_data, 
                'providerRef': providerRef, 'thirdPartyCode': 'AKRN', 
                'customerDtNumber': customerDtNumber, 'ip':ip}

    # thirdPartyCode and providerRef: to be generated from the validation response
            
    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv

def jos_prepaid(login_id, customer_account_id, service_id, 
                   amount, request_id, customerDtNumber, providerRef):
    
    # request_id = random.randrange(10000000, 99999999)

    checksum = (str(login_id) + "|" + service_id + "|" 
                + private_key + "|" + str(customer_account_id) + "|" 
                + str(request_id) + "|" + str(amount)
               )

    checksum_data = hash_data(checksum)

    url = get_config('SERVICES', 'electic_recharge')

    payload = {'loginId': login_id, 'authId': auth_login, 'key': public_key, 
                'customerAccountId': customer_account_id, 
                'serviceId': service_id, 'amount': amount, 
                'requestId': request_id, 
                'checksum': checksum_data, 
                'providerRef': providerRef, 'thirdPartyCode': 'AKRN', 
                'customerDtNumber': customerDtNumber, 'ip':ip}

    # thirdPartyCode and providerRef: to be generated from the validation response
            
    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv


def kaduna_prepaid(login_id, customer_account_id, service_id, 
                   amount, request_id, customerDtNumber, providerRef):
    
    # request_id = random.randrange(10000000, 99999999)

    checksum = (str(login_id) + "|" + service_id + "|" 
                + private_key + "|" + str(customer_account_id) + "|" 
                + str(request_id) + "|" + str(amount)
               )

    checksum_data = hash_data(checksum)

    url = get_config('SERVICES', 'electic_recharge')

    payload = {'loginId': login_id, 'authId': auth_login, 'key': public_key, 
                'customerAccountId': customer_account_id, 
                'serviceId': service_id, 'amount': amount, 
                'requestId': request_id, 
                'checksum': checksum_data, 
                'providerRef': providerRef, 'thirdPartyCode': 'AKRN', 
                'customerDtNumber': customerDtNumber, 'ip':ip}

    # thirdPartyCode and providerRef: to be generated from the validation response
            
    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv


def kano_prepaid(login_id, customer_account_id, service_id, 
                   amount, request_id, customerDtNumber, providerRef):
    
    # request_id = random.randrange(10000000, 99999999)

    checksum = (str(login_id) + "|" + service_id + "|" 
                + private_key + "|" + str(customer_account_id) + "|" 
                + str(request_id) + "|" + str(amount)
               )

    checksum_data = hash_data(checksum)

    url = get_config('SERVICES', 'electic_recharge')

    payload = {'loginId': login_id, 'authId': auth_login, 'key': public_key, 
                'customerAccountId': customer_account_id, 
                'serviceId': service_id, 'amount': amount, 
                'requestId': request_id, 
                'checksum': checksum_data, 
                'providerRef': providerRef, 'thirdPartyCode': 'AKRN', 
                'customerDtNumber': customerDtNumber, 'ip':ip}

    # thirdPartyCode and providerRef: to be generated from the validation response
            
    rh = RequestHandler(url, method=1, data=payload)
    retv = rh.send()
    return retv



