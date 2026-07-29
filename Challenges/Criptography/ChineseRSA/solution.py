from sympy.ntheory.modular import crt
from sympy import integer_nthroot

n = []
c = []
e = 17

with open("challenge.txt", "r") as f:
    for line in f:
        line = line.strip()

        if line.startswith("n"):
            valore = line.split("=")[1].strip()
            n.append(int(valore))

        elif line.startswith("c"):
            valore = line.split("=")[1].strip()
            c.append(int(valore))

m_to_e = crt(n, c)

m = integer_nthroot(m_to_e[0], e)[0]

print(m.to_bytes((m.bit_length() + 7) // 8, "big").decode())