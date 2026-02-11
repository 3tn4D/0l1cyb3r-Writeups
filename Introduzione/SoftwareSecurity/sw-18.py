from pwn import *

HOST = "software-18.challs.olicyber.it"
PORT = 13001
r = remote(HOST, PORT)

r.recvuntil(b"... Invia un qualsiasi carattere per iniziare ...")
r.sendline()

for i in range(100):
    r.recvuntil(b"0x")

    val = r.recvuntil(b" ").decode().strip()
    data = r.recv(100)

    if b"unpacked" in data and b"32-bit" in data:
        r.send(u64(val))
    elif b"upacked" in data and b"64-bit" in data:
        r.send(u64(val))
    elif b"packed" in data and b"32-bit" in data:
        r.send(p32(int(val, 16)))
    elif b"packed" in data and b"64-bit" in data:
        r.send(p64(int(val, 16)))

print(r.recv(100).decode())