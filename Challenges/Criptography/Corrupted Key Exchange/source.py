import os
import json
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
from signal import alarm as timeout
FLAG = b"????"


def find_flag(i):
    g, p = "1", "3"
    g, p = int(g, 16), int(p, 16)

    Alice_public = 1

    Bob_private = i

    Bob_Shared_secret = pow(Alice_public, Bob_private, p)

    key = (Bob_Shared_secret % (2**(8*16) - 1)).to_bytes(16, 'big')

    decrypt_flag(key, "HZJNGZczSDtWjBLe4zYaVi5U5CmD2lhwBpPRu4e3PLw=")


def decrypt_flag(key, ciphertext_b64):
    ciphertext = b64decode(ciphertext_b64)
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = unpad(cipher.decrypt(ciphertext), 16)
    print("flag: " + plaintext.decode().strip())


def main():
    for i in range(4):
        # si cercano tutti i valori da 0 a p fino a trovare la chiave privata
        try:
            find_flag(i)
        except Exception:
            continue

if __name__ == '__main__':
    timeout(300)
    main()
