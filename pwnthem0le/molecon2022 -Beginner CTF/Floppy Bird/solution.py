import requests
import json

url = "http://floppybird.challs.olicyber.it/"

data = requests.get(url + "get-token")
token = json.loads(data.text)["token"]

for i in range(1001):
    score = {"score":i, "token":token}
    r = requests.post(url + "update-score", json=score)

    if i % 100 == 0:
        print(i)

print(json.loads(r.text)["flag"])