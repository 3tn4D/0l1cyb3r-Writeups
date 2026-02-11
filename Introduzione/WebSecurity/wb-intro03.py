import requests

headers = {"X-Password" : "admin"}
r = requests.get("http://web-03.challs.olicyber.it/flag", headers=headers)

print(r.text)
