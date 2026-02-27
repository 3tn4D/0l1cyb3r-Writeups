from z3 import *

hash = "630:624:622:612:609:624:623:610:624:624:567:631:638:639:658:593:546:605:607:585:648:636:635:704:702:687:687:682:629:699:633:639:634:637:578:622:620:617:606:615:568:633:589:587:645:639:653:654:633:634"
hash = hash.split(":")

def encrypt(plaintext):
    ciphertext = []
    for i in range(len(plaintext)):
        print("\ni: ", i)
        
        c = 0
        for j in range(7):
            c += ord(plaintext[(i + j) % len(plaintext)])
            
            print("j: ", j, end=" | ")
            print("c: ", c)

        ciphertext.append(c)
    return ciphertext

def decrypt(cipher):
    n = len(cipher)
    s = Solver()

    x = [Int(f"x_{i}") for i in range(n)]

    for i in range(n):
        s.add(
            Sum([x[(i+j) % n] for j in range(7)]) == cipher[i]
        )

    for i in range(n):
        s.add(x[i] >= 32, x[i] <= 126)

    if s.check() == sat:
        m = s.model()
        plaintext = ''.join(chr(m[x[i]]) for i in range(n))
        return plaintext


dec = decrypt(hash)
print("flag{" + dec + "}")