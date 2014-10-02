import unittest
import os
import requests
import json

class TestAPI(unittest.TestCase):

	def test_api(self):
		#testing basic functionality of API

		email = "test@test.com"
		password = "test"

		url = "http://recruiting-api.nextcapital.com/users/sign_in"
		data = {"email": email, "password": "fake_pw"}

		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

		r = requests.post(url, data=json.dumps(data), headers=headers)
		
		self.assertEqual(r.json()['error'], "Password is not valid.")

		data = {"email": email, "password": password}

		r = requests.post(url, data=json.dumps(data), headers=headers)
		
		self.assertEqual(r.json()['email'], "test@test.com")
		self.assertEqual(r.json()['id'], 124)




if __name__ == '__main__':
	unittest.main()