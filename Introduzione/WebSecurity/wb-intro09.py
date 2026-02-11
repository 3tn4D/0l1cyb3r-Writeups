import requests

headers = {"Content-Type": "application/json"}
payload = dict(username = "admin", password = "admin")

r = requests.post("http://web-09.challs.olicyber.it/login", json = payload, headers = headers)

print(r.text)
