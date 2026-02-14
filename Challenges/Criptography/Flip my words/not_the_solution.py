from pwn import *
from base64 import b64decode, b64encode

r = remote("flip.challs.olicyber.it", 10603)

# Encrypt
r.recv(512)
r.sendline(b"1")
r.recv(100)

r.sendline(b'A'*7 + b'{"admin": true, "msg": "Dammi la flaaag!     "}')

cipher_bytes = r.recvuntil(b'\n').decode().split(":")[1].strip()
cipher_bytes = b64decode(cipher_bytes)
r.recv(512)

for i in range(0, len(cipher_bytes), 16):
    print(i//16)

# Decrypt con IV parte del ciphertext ricevuto
r.sendline(b"2")

IV_block = cipher_bytes[16:32]
cookie_blocks = cipher_bytes[32:80]

r.recvuntil(b"Inserisci un ordine:")
r.sendline(b64encode(cookie_blocks))

r.recvuntil(b"IV:")
r.sendline(b64encode(IV_block))

print(r.recvall(timeout=2))

# ----------- part1 -------------- -------------------- part2 --------------------- -- part3 --
# {"admin": false, "msg": "AAAAAAA {"admin": true, "msg": "Dammi la flaaag!"}       "}

#|         len = 32              | |                 len = 48                     | | len = 2 |

#                 |      IV      | |                  cookie                      |
#                 |    (16-32)   | |                 (32-80)                      |