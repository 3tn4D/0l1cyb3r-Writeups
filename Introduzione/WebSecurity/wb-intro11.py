import requests
import json

s = requests.session()

payload = {"username" : "admin", "password" : "admin"}

csrf = json.loads(s.post("http://web-11.challs.olicyber.it/login", json = payload).text)["csrf"]
flag = ""

for i in range(0, 4):
    url = "http://web-11.challs.olicyber.it/flag_piece?index=" + str(i) + "&csrf=" + str(csrf)
    r = s.get(url)

    flag += json.loads(r.text)["flag_piece"]

    csrf = json.loads(s.post("http://web-11.challs.olicyber.it/login", json = payload).text)["csrf"]

print(flag)
