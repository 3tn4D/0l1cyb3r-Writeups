import random
from Cryptodome.Cipher import AES
from Cryptodome.Util.number import long_to_bytes

p = int("d958c484ef58570da9588575bc59a38012d0dcfb007215ef02f45dd9a2c6e4e3", 16)
g = int("02", 16)
A = int("4cf7faf8578893a695248a4e9811e77ca7d924cd0f14d378aba70fc18386342a", 16)
b = 131313231323
B = pow(g, b, p)

key = long_to_bytes(pow(A, b, p))[:32]

iv = bytes.fromhex("ed1083ff18c38f134bdcfabc2fe06363")
m  = bytes.fromhex("ae93e08e3860aac7cd1656ec434166acc9c388274063f6940b8f160b3c48b7d44f101c5326f2d4720a58ee8f9b9fd8f9")

cipher = AES.new(key, AES.MODE_CBC, iv)
print(cipher.decrypt(m).decode())