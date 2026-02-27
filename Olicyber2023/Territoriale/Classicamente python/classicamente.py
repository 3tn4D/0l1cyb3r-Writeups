import random


def encrypt(data):
    n = 4
    data += "_"*(n - (len(data) % n))
    cols = [data[i::n] for i in range(n)]
    return "".join(cols)

def decrypt(ciphertext):
    n = 12
    
    data = list(ciphertext)

    cols = []
    for i in range(n):
        cols.append(ciphertext[i::n])

    print("".join(cols).strip("____"))


#flag = open("../flags.txt", "r").read().strip()
#enc = encrypt(flag)
#print(enc)

flag = open("classicamente.txt").read().strip()
dec = decrypt(flag)