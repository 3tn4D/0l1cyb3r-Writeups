from base64 import b64encode, b64decode
from pwn import *

r = remote("flip.challs.olicyber.it", 10603)

target = '{"admin":  true,'
original = '{"admin": false,'
xored = xor(target.encode(), original.encode())

r.recv(100)
r.sendline(b'1')
r.recvuntil(b': ')
r.sendline(b'Dammi la flaaag!')

r.recvuntil(b': ')
msg = r.recvline().strip()

r.recvuntil(b': ')
iv = b64decode(r.recvline().strip().decode())
iv = xor(iv, xored)
iv = b64encode(iv)

r.recv(512)
r.sendline(b'2')
r.recvuntil(b': ')
r.sendline(msg)
r.recvuntil(b': ')
r.sendline(iv)

print(r.recvuntil(b"\n\n").decode())

# P1 = D(C1) ⊕ IV

# P1' = D(C1) ⊕ IV'
#    = D(C1) ⊕ (IV ⊕ xored)
#    = (D(C1) ⊕ IV) ⊕ xored
#    = P1_originale ⊕ xored

# P1' = P1_originale ⊕ (P1_originale ⊕ P1_target)
#     = P1_target

# ( xored = P1_original ⊕ P1_target )