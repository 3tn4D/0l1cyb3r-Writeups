# https://crypto.stackexchange.com/questions/33561/cube-root-attack-rsa-with-low-exponent#33571

import gmpy2
from Cryptodome.Util.number import long_to_bytes

f = open("ct.txt", "r")
n = int(f.readline().split("= ")[1].strip())
e = int(f.readline().split("= ")[1].strip())
ciphertext = int(f.readline().split("=")[1].strip())
f.close()

k = 0
while True:
    candidate = ciphertext + k * n
    root, is_exact = gmpy2.iroot(candidate, e)  # radice e-esima intera
    
    if is_exact:
        plaintext = long_to_bytes(root).decode()
        print(plaintext)
        break
    
    k += 1