#
# Using command line you can do this:
#     curl -d '{"message":"hello"}' -H "Content-Type: application/json" -X POST localhost:5005/webhooks/rest/webhook
#
import json
import requests
import ast

while True:
    message = input('Write something :\n')
    headers = {'Content-Type': 'application/json'}
    payload = {'message': message}
    r = requests.post('http://localhost:5005/webhooks/rest/webhook', headers=headers, data=json.dumps(payload))
    #assert r.status_code == 200
    r = ast.literal_eval(r.text)
    # print(r.text[35:-3])
    if len(r)==1:
        if r[0].get('text'):
            print(r[0]['text'])
        if r[0].get('image'):
            print(r[0]['image'])
    else:
        for i in range(len(r)):
            if r[i].get('text'):
                print(r[i]['text'])
            if r[i].get('image'):
                print(r[i]['image'])
