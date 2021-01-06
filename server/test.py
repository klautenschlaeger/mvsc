import json

import requests


url = 'http://localhost:5000/mv/update'
myobj = {'somekey': 'somevalue'}

requests.post('http://localhost:5000/mv/update', json={'key':'value'})
#print the response text (the content of the requested file):

print()
