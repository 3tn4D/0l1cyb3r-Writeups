from pwn import *

exe = ELF("./sw-19")

r = remote("software-19.challs.olicyber.it", 13002)

r.recvuntil(b"... Invia un qualsiasi carattere per iniziare ...")
r.sendline()

while True:
    r.recvuntil(b" ")
    fun = r.recvuntil(b": ").decode().strip().replace(":", "")

    if fun not in exe.sym:
        break

    addr = exe.sym[fun]

    r.sendline(hex(addr))

print(r.recv(512).decode())