from base64 import b64encode, b64decode
from pwn import *
import re
import json

r = remote("based.challs.olicyber.it", 10600)

r.recvuntil(b"\n\n")

while True:
    try:
        t = r.recvuntil(b"risposta!").decode()
    except:
        break
    print(t)

    # estraggo il JSON con regex
    m = re.search(r'\{.*"message":\s*"(.*?)".*\}', t)
    if not m:
        break

    msg = m.group(1)

    if "da base64" in t:
        decoded = b64decode(msg.encode())
        answer = decoded.decode()

    elif "da esadecimale" in t:
        answer = bytes.fromhex(msg).decode()

    elif "da binario" in t:
        answer = int(msg, 2).to_bytes((len(msg) + 7) // 8, "big").decode()

    elif "a base64" in t:
        answer = b64encode(msg.encode()).decode()

    elif "a esadecimale" in t:
        answer = msg.encode().hex()

    elif "a binario" in t:
        answer = ''.join(f'{ord(b):08b}' for b in msg)
        if answer[0] != '1':
            i = 0
            while answer[i] != '1':
                answer = answer[i+1:]

    else:
        break

    json_dict = {"answer": answer}
    print(json_dict)
    r.sendline(json.dumps(json_dict).encode())

flag = r.recv(1000)
print(flag.decode())
