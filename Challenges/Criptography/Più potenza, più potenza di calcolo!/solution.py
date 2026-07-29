from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

def factorial(x):
    prod = 1
    for i in range (1,x+1):
        prod = prod * i
    return prod

a = 3
b = 8
p = 159043501668831001976189741401919059600158436023339250375247150721773143712698491956718970846959154624950002991005143073475212844582380943612898306056733646147380223572684106846684017427300415826606628398091756029258247836173822579694289151452726958472153473864316673552015163436466970719494284188245853583109
g = -1 # factorial(p-1) = -1 perchè A = g^b mod p (stessa cosa per B) e se g vale p-1 allora mod p varrà sempre -1

flag = "flag{...}"

def getDHkey():
    A = pow(g,a,p)
    B = pow(g,b,p)
    K = pow(B,a,p)

    return K

def decrypt(f, k):
    
    key = fakePadding(str(k))
 
    chiave = bytes(key, "utf-8")
    cipher = AES.new(chiave, AES.MODE_ECB)
    decryptedFlag = cipher.decrypt(f)
    return decryptedFlag

def fakePadding(k):
    if (len(k) > 16):
        raise ValueError('La tua chiave è più lunga di 16 byte')
    else:
        if len(k) == 16:
            return k
        else:
            missingBytes = 16 - len(k)
            for i in range(missingBytes):
                k = ''.join([k,"0"])
            return k


ciphertext = bytes.fromhex("b5609cfbad99f1b20ec3a93b97f379d8426f934ffcb77d83ea9161fefa78d243")

K = getDHkey()

print(decrypt(ciphertext, K).decode().strip())