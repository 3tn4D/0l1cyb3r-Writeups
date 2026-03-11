from pwn import *

r = remote("spg.challs.olicyber.it", 38052)

# iv | username=aaaaaaa | ;index0=0;index1 | =1;index2=2;inde | x3=3;a=aaaaaaaa\x01 | ;index0={rand};index1={rand};index2={rand};index3={rand}

payload = "aaaaaaa;index0=0;index1=1;index2=2;index3=3;a=aaaaaaaa\x01"

# 1) Generare un token per user aaaaaaa, così lo aggiunge all'array
# 2) Generare un token passando come username aaaaaaa;index0=0;index1=1;index2=2;index3=3;a=aaaaaaaa\x01
# 3) Prendere l'esadecimale e rimuovere gli ultimi 3 blocchi, così da far rimanere solo gli index desiderati


r.sendlineafter(b"> ", b"1")
r.sendlineafter(b"Username? ", b"aaaaaaa")

r.sendlineafter(b"> ", b"1")
r.sendlineafter(b"Username? ", payload.encode())
r.recvuntil(b"token: ")
token = r.recvline().decode().strip()

token_arr = [token[i:i+32] for i in range(0, len(token) - (32*3), 32)]

new_token = "".join(token_arr)
r.sendlineafter(b"> ", b"2")
r.sendlineafter(b"Token? ", new_token.encode())
print(r.recvline().decode().replace("-", ""))