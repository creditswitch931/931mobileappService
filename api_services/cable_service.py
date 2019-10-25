import base64
import bcrypt
import requests
import json
import random
from .api_lib import get_config, hash_data
from applib.api.resp_handler import Response, RequestHandler, FormHandler



def startimes_validate(login_id, public_key, private_key, smart_card_code):
	checksum = str(login_id) + "|" + private_key + "|" + str(smart_card_code)
	checksum_data = hash_data(checksum)

	startimes_validate = get_config('SERVICES')
	request_url = startimes_validate['star_validate']

	payload = {'loginId': login_id, 'key': public_key, 'smartCardCode': smart_card_code, 
				'checksum': checksum_data}

	rh = RequestHandler(url, method=1, data=payload)
	retv = rh.send()
	return retv

	# r = requests.post(request_url, data=payload) 
	# return r.json()


def startimes_vending(login_id, public_key, private_key, smart_card_code, fee):
	transaction_ref = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
	checksum = str(login_id) + "|" + private_key + "|" + str(smart_card_code) + "|" + str(fee)
	checksum_data = hash_data(checksum)

	startimes_vending = get_config('SERVICES')
	request_url = startimes_vending['star_vending']

	payload = {'loginId': login_id, 'key': public_key, 'smartCardCode': smart_card_code, 
				'fee': fee, 'transactionRef': transaction_ref, 'checksum': checksum_data}

	rh = RequestHandler(url, method=1, data=payload)
	retv = rh.send()
	return retv


def multichoice_validate(login_id, public_key, private_key, customer_no, service_id):
	checksum = str(login_id) + "|" + private_key + "|" + str(customer_no)
	checksum_data = hash_data(checksum)

	multichoice_validate = get_config('SERVICES')
	request_url = multichoice_validate['multi_validate']

	payload = {'loginId': login_id, 'key': public_key, 'customerNo': customer_no, 
				'serviceId': service_id, 'checksum': checksum_data}

	rh = RequestHandler(url, method=1, data=payload)
	retv = rh.send()
	return retv



def multichoice_fetch_product(login_id, public_key, service_id):
	multichoice_fetch_product = get_config('SERVICES')
	request_url = multichoice_fetch_product['multi_fetch_prod']

	payload = {'loginId': login_id, 'key': public_key, 'serviceId': service_id}

	rh = RequestHandler(url, method=1, data=payload)
	retv = rh.send()
	return retv



def multichoice_fetch_product_addons(login_id, public_key, service_id):
	multichoice_fetch_product_addons = get_config('SERVICES')
	request_url = multichoice_fetch_product['multi_fetch_prod']

	payload = {'loginId': login_id, 'key': public_key, 'serviceId': service_id}

	rh = RequestHandler(url, method=1, data=payload)
	retv = rh.send()
	return retv



def multichoice_vending(login_id, public_key, private_key, customer_no, customer_name, service_id, amount, invoice_period):
	transaction_ref = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
	checksum = str(login_id) + "|" + private_key + "|" + customer_no + "|" + transaction_ref + "|" + str(amount);
	checksum_data = hash_data(checksum)

	multichoice = multichoice_fetch_product(login_id, public_key, service_id)
	
	product_codes = []
	for key, value in multichoice.items():
		if key == 'statusDescription':
			for key, items in value.items():
				for x in items:
					product_codes.append(x['code'])

	multichoice_vending = get_config('SERVICES')
	request_url = multichoice_vending['multi_recharge']

	payload = {'loginId': login_id, 'key': public_key, 'serviceId': service_id, 
				'checksum': checksum_data, 'transactionRef': transaction_ref, 
				'customerNo': customer_no, 'customerName': customer_name, 
				'productCodes': product_codes, 'amount': amount, 'invoicePeriod': invoice_period}

	rh = RequestHandler(url, method=1, data=payload)
	retv = rh.send()
	return retv



if __name__ == '__main__':
	startimes_validate(38457, "j6kHi1NXAOjrHFk0", "XY1t9Y159hWJaETD", "92000002866")
