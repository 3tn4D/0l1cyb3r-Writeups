from pwn import *

def xor(a, b):
    return bytes(x^y for x, y in zip(a, b))

r = remote("sandwichmaster.challs.olicyber.it", 30996)

msg = b'Im so good with sandwiches they call me mr Krabs'.hex()
blocks = [msg[i:i+32] for i in range(0, len(msg), 32)]

# Al posto di mandare tutto assieme lo mandi a pezzi
r.recv(512)
r.sendline(b"1")
r.recvuntil(b"gimme m: ")
r.sendline(blocks[0].encode())
tag = r.recvline().decode().split("= '")[1].strip()[:-1]

new_block = xor(bytes.fromhex(blocks[1]), bytes.fromhex(tag)).hex()

r.recv(512)
r.sendline(b"1")
r.recvuntil(b"gimme m: ")
r.sendline(new_block.encode())
tag = r.recvline().decode().split("= '")[1].strip()[:-1]

new_block = xor(bytes.fromhex(blocks[2]), bytes.fromhex(tag)).hex()

r.recv(512)
r.sendline(b"1")
r.recvuntil(b"gimme m: ")
r.sendline(new_block.encode())
tag = r.recvline().decode().split("= '")[1].strip()[:-1]

# Mandi il tag del messaggio
r.recv(512)
r.sendline(b"2")
r.recvuntil(b"gimme your tag: ")
r.sendline(tag.encode())
print(r.recvline().decode())