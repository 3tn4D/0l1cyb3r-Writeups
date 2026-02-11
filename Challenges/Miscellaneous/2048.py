from pwn import *

r = remote("2048.challs.olicyber.it", 10007)

r.recvuntil(b":")

for i in range(2048):
    print(f"Operazione {i}")

    data = r.recvuntil(b" ").decode().strip()

    nums = r.recv(100).decode().split()
    res = 0

    a, b = map(int, nums)

    if data == "SOMMA":
        res = a + b
    elif data == "DIFFERENZA":
        res = a - b
    elif data == "PRODOTTO":
        res = a * b
    elif data == "DIVISIONE_INTERA":
        res = a // b
    elif data == "POTENZA":
        res = pow(a, b)

    r.sendline(str(res).encode())

print(r.recv(512).decode())