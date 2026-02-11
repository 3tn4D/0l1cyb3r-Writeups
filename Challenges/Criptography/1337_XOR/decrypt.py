import os

# Conoscendo una parte della stringa finale e siccome la lunghezza della chiave
# è 6 ripetuto per 7 volte, si fa una xor e si prova un ciclo for con la chiave
# trovata lasciando dei buchi, poi si deduce il 6° carattere e lo si aggiunge, trovando la flag

FLAG = b"flag{1"

def xor(a, b):
    return bytes([ x ^ y for x,y in zip(a,b) ])

encrypted_flag = ""
with open("output.txt", "r") as output_file:
    encrypted_flag = output_file.read().split()[1]
    encrypted_flag = bytes.fromhex(encrypted_flag)

print(encrypted_flag)
print(len(encrypted_flag))

print()

key = xor(FLAG, encrypted_flag[:6])

for i in range(0, 37, 6):
    print(xor(key, encrypted_flag[i:i+6]).decode(), end="")

print()