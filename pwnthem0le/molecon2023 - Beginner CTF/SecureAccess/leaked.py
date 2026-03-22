# uncompyle6 version 3.9.3
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.13.5 (main, Jun 25 2025, 18:55:22) [GCC 14.2.0]
# Embedded file name: leaked.py
# Compiled at: 2023-10-26 19:39:19
# Size of source mod 2**32: 304 bytes
import hashlib, json, base64

def generate_token(nonce: str):
    username = "admin"
    secret = hashlib.sha256(username.encode() + nonce.encode()).hexdigest()
    bundle = {'user':username, 
     'secret':secret}
    return base64.b64encode(json.dumps(bundle).encode())

token = generate_token("53331FA5-4D79-45C9-B9FC-DA108A439286")
print(token)