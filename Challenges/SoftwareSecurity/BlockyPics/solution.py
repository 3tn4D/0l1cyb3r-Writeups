from ctypes import CDLL
from pwn import *
from Cryptodome.Cipher import AES
libc = CDLL('libc.so.6') # Include libreria rand() di C

def init():
    libc.srand(58913)
    v1 = libc.rand()
    libc.srand(v1 % 10000)
    v2 = libc.rand()
    libc.srand(v2)
    v2 = libc.rand()
    libc.srand(v2)
    v2 = libc.rand()
    libc.srand(v2)

def gen1(array: bytearray, length: int):
    rnd = libc.rand()
    var = (rnd // length) & 0xffffffff

    if length > 0:
        for idx in range(length):
            base_byte = array[(rnd % length + idx) % length]
            rand_byte = libc.rand()

            array[idx] = base_byte ^ (rand_byte & 0Xff)

            var = rand_byte

    return var

def gen2(array, length):
    if length > 0:
        for idx in range(length):
            rnd = libc.rand()
            
            base_byte = array[rnd % length]
            rand_byte = libc.rand()

            array[idx] = base_byte ^ (rand_byte & 0xff)



def generateKey(array, length):
    if libc.rand() & 1 != 0:
        gen1(array, length)
    else:
        gen2(array, length)
    

r = remote("blockypics.challs.olicyber.it", 10805)
r.recvline()

blocks = []
for i in range(5):
    r.recvline()
    blocks.append(bytes.fromhex(r.recvline().decode().strip()))

res = []
init()

for i in blocks:
    key = bytearray(32)
    generateKey(memoryview(key), 32)
    iv = bytearray(16)
    generateKey(memoryview(iv), 16)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    res.append(cipher.decrypt(i))

c = 0
for i in res:
    with open(f"img{c}.jpg", "wb") as img:
        img.write(i)
    
    c += 1