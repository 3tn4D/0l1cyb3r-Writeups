import requests

cookies = dict(password = "admin")                          #corrispondente a {"password" : "admin"}
r = requests.get("http://web-05.challs.olicyber.it/flag", cookies = cookies)

print(r.text)
