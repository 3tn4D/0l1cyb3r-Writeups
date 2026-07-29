import os

from secret import p,q,FLAG

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from random import randint

iv = os.urandom(16)

n = p*q
g = 2
a = randint(1, n)
b = randint(1, n)
A = pow(g, a, n)
B = pow(g, b, n)

assert pow(A, b, n) == pow(B, a, n)

key = pow(A, b, n)
key = key.to_bytes(-(key.bit_length()//-8), "big")[:16]
enc_flag = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(FLAG, 16))

with open("output.txt", "w") as f:
    f.write(f"n={n}\ng={g}\nA={A}\nB={B}\n\nIV={iv.hex()}\nFLAG={enc_flag.hex()}")