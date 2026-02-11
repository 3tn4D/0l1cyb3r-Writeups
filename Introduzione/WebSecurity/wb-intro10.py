import requests

r = requests.options("http://web-10.challs.olicyber.it/")

print(r.headers)

r = requests.put("http://web-10.challs.olicyber.it/")

print(r.headers)
