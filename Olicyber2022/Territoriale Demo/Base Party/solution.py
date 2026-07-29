from base64 import b32decode, b64decode

ct = open("encoded.txt", "r").read()

while "flag" not in ct:
    ct = b64decode(b32decode(bytes.fromhex(ct))).decode()

print(ct)