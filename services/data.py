import base64
import bcrypt
import requests
import json
import random
from api_test import get_config, hash_data
from applib.api.resp_handler import Response, RequestHandler, FormHandler



def data_vending(login_id, public_key, private_key, amount, recipient, provider):
	request_id = random.randrange(10000000, 99999999)
	request_id = str(request_id)

	if provider == "airtel":
		service_id = "D01D"
	elif provider == "9mobile":
		service_id = "D02D"
	elif provider == "globacom":
		service_id = "D03D"
	elif provider == "mtn":
		service_id = "D04D" 

	checksum = (str(login_id) + "|" + request_id + "|" + service_id + "|" + str(amount) + "|" +
				private_key + "|" + recipient)

	checksum_data = hash_data(checksum)

	data_vending = get_config('url')
	request_url = data_vending['airtime']

	payload = {'loginId': login_id, 'key': public_key, 'requestId': request_id, 'serviceId': service_id, 
				'amount': amount, 'recipient' : recipient , 'checksum': checksum_data} 

	rh = RequestHandler(url, method=1, data=payload)
	retv = rh.send()
	return retv


def data_plan(login_id, public_key, service_id):
	data_plan = get_config('url')
	request_url = data_plan['data_plan']

	payload = {'loginId': login_id, 'key': public_key, 'serviceId': service_id}

	rh = RequestHandler(url, method=0, data=payload)
	retv = rh.send()
	return retv



if __name__ == '__main__':
	main()