from pwn import *
import re

context.log_level = "error"

"""
| input | rand | flag |
    ^
    |
keystream = input xor cipher_input

| flag | rand | input |
    ^
    |
keystream = flag xor cipher_flag => flag = keystream xor cipher_flag
"""

n = 0
while True:
    n += 16
    payload = b"a" * n

    arr = []
    dup = []

    while True:
        r = remote("sme.challs.olicyber.it", 10506)

        r.sendlineafter(b"invia! ", payload)
        r.recvuntil(b"Ciphertext: ")

        ciphertext = bytes.fromhex(r.recvline().strip().decode())[:n]

        if ciphertext in arr and ciphertext not in dup:
            dup.append(ciphertext)
        else:
            arr.append(ciphertext)

        if len(dup) == 2:
            break
    
    flag = bytes.fromhex(xor(xor(payload.hex().encode(), dup[0]), dup[1]).decode())
    if b"}" in flag:
        match = re.search(rb"flag\{.*?\}", flag)
        if match:
            print(match.group().decode())
            break