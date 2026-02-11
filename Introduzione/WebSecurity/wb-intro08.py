import requests

headers = {"Content-Type": "application/x-www-form-urlencoded"}
payload = dict(username = "admin", password = "admin")

r = requests.post("http://web-08.challs.olicyber.it/login", data = payload, headers = headers)

print(r.text)
