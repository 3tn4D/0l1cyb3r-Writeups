from Crypto.Util.number import getStrongPrime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha1
import random
from secret import flag

p = getStrongPrime(1024)
g = 2

def gen_key(g, p):
    a = random.randint(1,p)
    return a, pow(g,a,p)

print(p)

b, B = gen_key(g, p)
a, A = gen_key(g, p)
sa, SA = gen_key(g, p)

print(f"Alice: my public key {A}")
print(f"Bob: my public key {B}")

challenge = (B*SA)%p

print(f"Alice: here's your challenge {challenge}")

shared_alice = (A*SA)%p
shared_bob = (A*challenge*pow(g,(p-1-b),p))%p

assert shared_alice == shared_bob

cipher = AES.new(sha1(shared_alice.to_bytes(128, byteorder = 'big')).digest()[:16], AES.MODE_ECB)
enc = cipher.encrypt(pad(flag,16))

print(f"Bob: here's the encrypted flag {enc.hex()}")
