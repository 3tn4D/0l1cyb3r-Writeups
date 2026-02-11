import requests

headers = {"Accept" : "application/xml"}
r = requests.get("http://web-04.challs.olicyber.it/users", headers = headers)

print(r.text)
