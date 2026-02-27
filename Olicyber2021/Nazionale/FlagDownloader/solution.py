import requests
import json

url = "http://flagdownloader.challs.olicyber.it/download/flag/"

flag = ""

c = "0"
while True:
    r = requests.get(url + c)

    data = json.loads(r.text.strip())
    c = data["n"]

    flag += data["c"]
    
    print(flag)