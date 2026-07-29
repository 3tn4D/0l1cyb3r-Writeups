#!/usr/bin/env python3
from Crypto.Util.number import long_to_bytes
from tqdm import tqdm
from pwn import *

context.log_level = "error"

flag = [0] * 200
while True:
    r = remote("time.challs.olicyber.it", 10505)

    for i in range(200):
        if flag[i] == 1:
            continue

        r.sendlineafter(b"> ", b"1")
        r.sendlineafter(b"? ", str(i).encode())
        
        f = r.recvline().decode().strip()
        try:
            bytes.fromhex(f)
        except:
            flag[i] = 1
    
    r.close()
    
    binf = int("".join(map(str, flag)), 2)
    flagf = long_to_bytes(binf)
    print(flagf)
    if b'flag{' in flagf:
        input()