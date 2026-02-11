from pwn import *

HOST = "software-17.challs.olicyber.it"
PORT = 13000
r = remote(HOST, PORT)

def somma(data):
    totale = 0
    for n in data:
        totale += int(n)
    return totale


r.recvuntil(b"... Invia un qualsiasi carattere per iniziare ...")
r.sendline()

for i in range(10):
    r.recvuntil(b"numeri")
    nums = r.recvuntil(b"]").decode().replace("]", "").replace("[", "").split(", ")

    nums = somma(nums)

    r.recv(100)
    r.sendline(str(nums).encode())

print(r.recv(100).decode())