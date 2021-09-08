#
# Using command line you can do this: 
#     curl -d '{"message":"hello"}' -H "Content-Type: application/json" -X POST localhost:5005/webhooks/rest/webhook
#
import json
import requests

headers = {'Content-Type': 'application/json'}
payload = {'message': 'Hello dude !'}
r = requests.post('http://localhost:5005/webhooks/rest/webhook', headers=headers, data=json.dumps(payload))
#assert r.status_code == 200
print(r.text)
