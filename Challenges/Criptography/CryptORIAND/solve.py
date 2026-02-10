from pwn import *

def find_ones_and(vet, s):
    s = list(s)
    for i in range(96):
        if any(b[i] == '1' for b in vet):
            s[i] = '1'
    return "".join(s)

def find_zeros_or(vet, s):
    s = list(s)
    for i in range(96):
        if all(b[i] == '0' for b in vet):
            s[i] = '0'
    return "".join(s)


risp = "Nope!"

while "Nope!" in risp:
    r = remote("cryptorland.challs.olicyber.it", 10801)

    rows = []
    for _ in range(10):
        rows.append(int(r.recvline().decode().strip()))

    rows = [bin(n)[2:].zfill(96) for n in sorted(rows)]

    secure_and = []
    secure_or = []

    # AND = lower numers
    # OR = higher numbers
    for b in rows:
        if b.count('1') > b.count('0'):
            secure_or.append(b)
        else:
            secure_and.append(b)

    key = ["?"] * 96
    key = find_ones_and(secure_and, key)
    key = find_zeros_or(secure_or, key)

    key = int(key.replace("?", "0"), 2)

    r.recv(512)
    r.sendline(str(key).encode())
    risp = r.recv(100).decode()

    r.close()

print(risp)
