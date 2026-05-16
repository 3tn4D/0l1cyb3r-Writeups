from pwn import *

r = remote("crc.challs.olicyber.it", 12201)

def crc16(data):
    res = 0xffff

    for c in data:
        val = ord(c) ^ (res >> 8)

        val &= 0xff
        val ^= (val >> 4)
        
        res = (val ^ (res << 8) ^ (val << 12) ^ (val << 5)) & 0xFFFF

    return res

check = 0
i = 0
while check != 0xe05b:
    check = crc16(str(i))
    i += 1
passwd = str(i-1).encode() + b"\x00"

r.recv(1000)
r.sendline(passwd)
print(r.recvline().decode().strip())