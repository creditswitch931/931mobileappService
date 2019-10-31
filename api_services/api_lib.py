import base64
import bcrypt
import requests
import json
import random
from configobj import ConfigObj


public_key='j6kHi1NXAOjrHFk0'
private_key="XY1t9Y159hWJaETD"


def get_config(header, key=None, filename='settings.cfg'):

	cfg = ConfigObj(filename)
	if not key:
		return cfg[header]

	return cfg[header][key]



def hash_data(checksum):
	checksum = checksum.encode("utf-8")
	value = bcrypt.hashpw(checksum, bcrypt.gensalt())

	encodedBytes = base64.b64encode(value)
	encodedStr = str(encodedBytes, "utf-8")
	return encodedStr



def merchant_details(login_id):
	checksum = str(login_id) + "|" + private_key
	checksum_data = hash_data(checksum)

	url = get_config('SERVICES', 'merchant')

	payload = {'loginId': login_id, 'key': public_key, 
				'checksum': checksum_data} 

	rh = RequestHandler(url, method=1, data=payload)
	retv = rh.send()
	return retv 



def requery_transaction(login_id, public_key, service_id):
	request_id = random.randrange(10000000, 99999999)

	url = get_config('SERVICES', 'requery')

	payload = {'loginId': login_id, 'key': public_key, 'requestId': request_id, 
				'serviceId': service_id}

	rh = RequestHandler(url, method=1, data=payload)
	retv = rh.send()
	return retv



 