#!/usr/bin/env python3.8

import os
import hmac
import time
import hashlib
from datetime import datetime
import random
import string
import requests

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
    print(expected_signature, signature)
    return hmac.compare_digest(expected_signature, signature)

site = "http://trulyrandomsignature.challs.olicyber.it/"
r = requests.get(site)

date_header = r.headers["Date"]
x_uptime = int(r.headers["X-Uptime"])

print("X-Uptime:", x_uptime)

server_now = datetime.strptime(date_header, "%a, %d %b %Y %H:%M:%S %Z")
server_now_ts = server_now.timestamp()
uptime = server_now_ts - x_uptime

seed = datetime.utcfromtimestamp(uptime).strftime("%Y-%m-%d %H:%M:%S")

print("\nUptime ricostruito:", uptime)
print("Seed ricostruito:", seed)

print(f"\nData: {server_now}\n")

random.seed(seed)

SUPER_SECRET_KEY = get_random_string(32)

if verify(r.cookies["user"], r.cookies["signature"], SUPER_SECRET_KEY):
  print("✔ Chiave corretta!") 
else:
  print("❌ Chiave sbagliata")
