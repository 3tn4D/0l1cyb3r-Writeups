from pwn import *
import os

# https://stackoverflow.com/questions/9049789/aes-encryption-key-versus-iv#9050752

r = remote("privateiv.challs.olicyber.it", 10021)

def encrypt(plaintext):
    r.recv(512)
    r.sendline(b'1')

    r.recv(100)
    r.sendline(plaintext.encode())

    return r.recvuntil(b'\n').decode().split(":")[1].strip()

def decrypt(chipertext):
    r.recv(512)
    r.sendline(b'2')

    r.recv(100)
    r.sendline(chipertext.encode())

    return r.recvuntil(b'\n').decode().split(":")[1].strip()

payload = os.urandom(16).hex() # la quantità di byte non importa, tanto viene fatto il pad e poi vengono presi solo i primi 16 byte
chipertext = bytes.fromhex(encrypt(payload))    

flag = bytes.fromhex(decrypt(chipertext[:16].hex() + "00" * 16 + chipertext[:16].hex()))
print(xor(flag[:16], flag[32:]))

# P1⊕P3

# P1=AES_DEC(K,C1)⊕K
# P3=AES_DEC(K,C1)

# P1⊕P3=(AES_DEC(K,C1)⊕K)⊕AES_DEC(K,C1)
# P1⊕P3=K