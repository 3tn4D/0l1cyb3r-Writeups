from pwn import *
from base64 import b64decode
from Cryptodome.Cipher import AES
from itertools import product
import string

charset = list(string.printable)

r = remote("bob.challs.olicyber.it", 10602)

r.recv(100)
r.sendline(b"00000000000")
r.recvuntil(b"?")

def encrypt(s, n):
    r.recv(100)
    r.sendline(b"1")
    r.recv(100)

    pad1 = b"\x00" * 11
    pad2 = b"\x00" * n
    pad3 = b"\x00" * n

    r.sendline(pad1 + pad2 + s.encode() + pad3)
    r.recvuntil(b'\n')

    enc = b64decode(r.recvuntil(b'\n')).hex()
    return [enc[i:i+32] for i in range(0, len(enc), 32)]

flag = "Alice: certo, eccola: flag{Sono_Stup3Nda"
while len(flag) < (16*2 + 15):
    for i in charset:
        blocks = encrypt(flag + i, (16*2 + 15)-len(flag))
        if blocks[3] == blocks[6]:
            flag += i
            print(flag)

            if flag[-1] == '}': exit(0)

            break

# --- blocco 0 --- --- blocco 1 --- --- blocco 2 --- --- blocco 3 --- --- blocco 4 --- --- blocco 5 --- --- blocco 6 ---
# Bob: 00000000000 0000000000000000 0000000000000000 000000000000000A 0000000000000000 0000000000000000 000000000000000A
# Bob: 00000000000 0000000000000000 0000000000000000 00000000000000Al 0000000000000000 0000000000000000 00000000000000Al
# Bob: 00000000000 0000000000000000 0000000000000000 Alice: certo, e  0000000000000000 0000000000000000 Alice: certo, e 
# Bob: 00000000000 0000000000000000 000000000000000A lice: certo, e § 0000000000000000 000000000000000A lice: certo, e §

#                                                           ^                                                   ^
#                                                           |                                                   |
#                                                       controllo                                           controllo
