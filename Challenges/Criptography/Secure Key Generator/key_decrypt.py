from hashlib import sha256
from datetime import datetime
import random
from itertools import cycle

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')

def generate_secure_key():
    dt = datetime(2021, 3, 21, 17, 37, 40)
    ts = int(datetime.timestamp(dt))
    h = sha256(int_to_bytes(ts)).digest()

    seed = int_from_bytes(h[32:])
    key = h[:32]
    
    random.seed(seed)
    for _ in range(32):
        key += bytes([random.randint(0, 255)])


    return key
    
key = generate_secure_key()
data = open("flag.enc", "rb").read()

with open("output.pdf", "wb") as f:
    for k, d in zip(cycle(key), data):
        f.write(bytes([k ^ d]))