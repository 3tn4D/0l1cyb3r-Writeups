from pathlib import Path
from Crypto.PublicKey import RSA
from itertools import combinations
import math

c = int.from_bytes(open("flag.txt.enc", "rb").read(), "big")

keys = {}

for pem_file in sorted(Path("keys").glob("key_*.pem")):
    with open(pem_file, "rb") as f:
        key = RSA.import_key(f.read())

    keys[pem_file.stem] = key

root = RSA.import_key(open("root.pem", "rb").read())
keys["root"] = root


# trova il massimo comune denominatore tra due chiavi che corrisponde a p
for nome1, nome2 in combinations(keys, 2):
    n1 = keys[nome1].n
    n2 = keys[nome2].n
    p = math.gcd(n1, n2)
    if p != 1:
        # ricava q delle due chiavi
        q1 = keys[nome1].n // p
        q2 = keys[nome2].n // p

        print(f"Fattore comune tra {nome1} e {nome2}")

        assert p * q1 == n1
        assert p * q2 == n2

        break

# servono solo i dati della chiave root.pem
e2 = keys[nome2].e
phi2 = (p - 1)*(q2 - 1)
d2 = pow(e2, -1, phi2)

flag = pow(c, d2, n2)
print(flag.to_bytes((flag.bit_length() + 7) // 8, "big"))