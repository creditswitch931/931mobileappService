import base64
import bcrypt
import requests
import json
import random
from services.api_test import get_config, hash_data


def electricity_validate(login_id, public_key, private_key, customer_account_id, service_id):
	checksum = str(login_id) + "|" + service_id + "|" + private_key + "|" + str(customer_account_id)
	checksum_data = hash_data(checksum)

	electricity_validate = get_config('SERVICES')
	request_url = electricity_validate['electic_validate']

	payload = {'loginId': login_id, 'key': public_key, 'customerAccountId': customer_account_id, 
				'serviceId': service_id, 'checksum': checksum_data}

	rh = RequestHandler(url, method=1, data=payload)
	retv = rh.send()
	return retv



def electricity_vending(login_id, public_key, private_key, customer_account_id, service_id, amount):
	request_id = random.randrange(10000000, 99999999)
	checksum = str(login_id) + "|" + service_id + "|" + private_key + "|" + str(customer_account_id) + "|" + str(request_id) + "|" + str(amount)
	checksum_data = hash_data(checksum)

	electricity_vending = get_config('SERVICES')
	request_url = electricity_vending['electic_recharge']

	# providerRef: to be generated from the validation response

	payload = {'loginId': login_id, 'key': public_key, 'customerAccountId': customer_account_id, 
				'serviceId': service_id, 'amount': amount, 'requestId': request_id, 'providerRef':'150144078049', 
				'checksum': checksum_data}

	rh = RequestHandler(url, method=1, data=payload)
	retv = rh.send()
	return retv 



def ikeja_prepaid_E01E(login_id, public_key, private_key, customer_account_id, service_id, amount):
	request_id = random.randrange(10000000, 99999999)

	checksum = str(login_id) + "|" + service_id + "|" + private_key + "|" + str(customer_account_id) + "|" + str(request_id) + "|" + str(amount)
	checksum_data = hash_data(checksum)

	electricity_vending = get_config('SERVICES')
	request_url = electricity_vending['electic_recharge']

	payload = {'loginId': login_id, 'key': public_key, 'customerAccountId': customer_account_id, 
				'serviceId': service_id, 'amount': amount, 'requestId': request_id, 
				'checksum': checksum_data, 'providerRef':'150144078049',}

	# providerRef: to be generated from the validation response

	electricity = electricity_validate(login_id, public_key, private_key, customer_account_id, service_id)

	for key, value in electricity.items():
		if key == 'details':
			for key, items in value.items():
				if key == 'details':
					payload['customerDtNumber'] = items['customerDtNumber']
			
	rh = RequestHandler(url, method=1, data=payload)
	retv = rh.send()
	return retv



def eko_prepaid_E05E(login_id, public_key, private_key, customer_account_id, service_id, amount):
	request_id = random.randrange(10000000, 99999999)

	checksum = str(login_id) + "|" + service_id + "|" + private_key + "|" + str(customer_account_id) + "|" + str(request_id) + "|" + str(amount)
	checksum_data = hash_data(checksum)

	electricity_vending = get_config('SERVICES')
	request_url = electricity_vending['electic_recharge']

	payload = {'loginId': login_id, 'key': public_key, 'customerAccountId': customer_account_id, 
				'serviceId': service_id, 'amount': amount, 'requestId': request_id, 
				'checksum': checksum_data, 'providerRef':'150144078049',}

	# providerRef: to be generated from the validation response

	electricity = electricity_validate(login_id, public_key, private_key, customer_account_id, service_id)

	for key, value in electricity.items():
		if key == 'details':
			for key, items in value.items():
				if key == 'details':
					payload['customerDtNumber'] = items['customerDtNumber']
			
	rh = RequestHandler(url, method=1, data=payload)
	retv = rh.send()
	return retv


 
def ibadan_prepaid_E08E(login_id, public_key, private_key, customer_account_id, service_id, amount):
	request_id = random.randrange(10000000, 99999999)

	checksum = str(login_id) + "|" + service_id + "|" + private_key + "|" + str(customer_account_id) + "|" + str(request_id) + "|" + str(amount)
	checksum_data = hash_data(checksum)

	electricity_vending = get_config('SERVICES')
	request_url = electricity_vending['electic_recharge']

	payload = {'loginId': login_id, 'key': public_key, 'customerAccountId': customer_account_id, 
				'serviceId': service_id, 'amount': amount, 'requestId': request_id, 
				'checksum': checksum_data, 'providerRef':'150144078049', 'thirdPartyCode': 'AKRN'}

	# thirdPartyCode and providerRef: to be generated from the validation response

	electricity = electricity_validate(login_id, public_key, private_key, customer_account_id, service_id)

	for key, value in electricity.items():
		if key == 'details':
			for key, items in value.items():
				if key == 'details':
					payload['customerDtNumber'] = items['customerDtNumber']
			
	rh = RequestHandler(url, method=1, data=payload)
	retv = rh.send()
	return retv




if __name__ == '__main__':
	ikeja_prepaid_E01E(38457, "j6kHi1NXAOjrHFk0", "XY1t9Y159hWJaETD", "0110347638", "E02E", 1000)

