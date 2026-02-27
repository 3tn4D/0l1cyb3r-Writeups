#!/bin/env python3

# pip3 install pwntools
from pwn import remote, context


def solve(stato, mosse):
    print(stato)
    print(mosse)

    res = ""
    
    for i, m in enumerate(mosse):
        elem = stato[m[0]]

        for _ in range(elem, 5):
            res += f"{i + 1} "

    print(res)

    return res.encode()


r = remote("test.challs.olicyber.it", 15004)
context.log_level = 'debug'
r.recvlines(20)

livello = r.recvline()
while livello.startswith(b"Livello"):
    stato = [int(_) for _ in r.recvline(False).decode().split()]
    mosse = []
    while True:
        s = r.recvline(False).decode()
        if s == "":
            break
        mosse.append(["ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(_) for _ in s.split()])
    res = solve(stato, mosse)
    r.sendline(res)
    r.recvlines(2)
    livello = r.recvline()

