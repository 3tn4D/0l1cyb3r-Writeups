from pwn import *

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

r = remote("modes.challs.olicyber.it", 10802)

ct = open("flag.enc", "r").read().strip()

iv = bytes.fromhex(ct[:32])
enc_hex = ct[32:]
enc_raw = bytes.fromhex(enc_hex) 

r.sendlineafter(b"ciphertext: ", enc_hex.encode())
pt_ecb = bytes.fromhex(r.recvline().decode().strip())

flag = xor_bytes(pt_ecb[:16], iv)
for i in range(16, len(enc_raw), 16):
    flag += xor_bytes(pt_ecb[i:i+16], enc_raw[i-16:i])

print(flag.decode())