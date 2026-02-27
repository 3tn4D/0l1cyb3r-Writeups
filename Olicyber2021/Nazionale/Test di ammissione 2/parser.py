#!/bin/env python3

# pip3 install pwntools
from pwn import remote, context


def solve(mosse, stato):
    res = ""

    return res.encode()

r = remote("test2.challs.olicyber.it", 15005)
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
    res = solve()
    r.sendline(res)
    r.recvlines(2)
    livello = r.recvline()
