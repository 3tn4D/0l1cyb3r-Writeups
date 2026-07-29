#!/usr/bin/env python3

import os

flag = os.getenv('FLAG', 'flag{redacted}')
assert flag.startswith('flag{') and flag.endswith('}')

def SmallCubeHash(m: bytes):
    def rot_left(word, k, n_bits = 12):
        return (word << k) & (2**n_bits - 1) | (word >> (n_bits - k))

    x = [0x243, 0xf6a, 0x888, 0x5a3]
    R = [7, 11]
    b = 6
    f = 24
    mask = 0xfff

    m += b"\x80"
    m += b"\x00" * (-len(m) % b)

    for i in range(0, len(m), b):
        block = int.from_bytes(m[i:i+b], "big")
        x[0] ^= ((block >> 36) & mask)
        x[1] ^= ((block >> 24) & mask)
        x[2] ^= ((block >> 12) & mask)
        x[3] ^= (block & mask)

        for _ in range(f):
            for j in range(2):
                x[2] = (x[2] + x[0]) & mask
                x[3] = (x[3] + x[1]) & mask
                x[0] = rot_left(x[0], R[j])
                x[1] = rot_left(x[1], R[j])
                x[0], x[1] = x[1], x[0]
                x[0] ^= x[2]
                x[1] ^= x[3]
                x[2], x[3] = x[3], x[2]

    output = (x[0] << 36) | (x[1] << 24) | (x[2] << 12) | x[3]

    return output.to_bytes(6, "big")

def xor(a,b):
    return bytes([x^y for x,y in zip(a,b)])

def CAMH(m, k):
    opad = b"\x5c"*len(k)
    ipad = b"\x36"*len(k)

    return SmallCubeHash(SmallCubeHash(m + xor(k, ipad)) + xor(k, opad))

if __name__ == "__main__":
    print("Ciao! Ho creato una mia variante di MAC, l'ho chiamata CAMH. Sei stato scelto per testare la sua sicurezza!")    
    m1 = bytes.fromhex(input("Inviami il primo messaggio (in hex): "))
    m2 = bytes.fromhex(input("Inviami il secondo messaggio (in hex): "))
    
    if m1 == m2:
        print("Troppo facile così!")
        exit()

    k = os.urandom(32)

    h1 = CAMH(m1, k)
    h2 = CAMH(m2, k)

    if h1 == h2:
        print("Wow, sei riuscito a rompere il mio MAC, eccoti il premio: " + flag)
    else:
        print("Allora direi che non ci sono problemi con il mio MAC.")
