from Cryptodome.Cipher import DES, AES, ChaCha20
from Cryptodome.Util.Padding import *
from Cryptodome import Random


# DES

key = bytes.fromhex("2ecff7b78d905c9d")
plain = "La lunghezza di questa frase non è divisibile per 8".encode("utf-8")
cipher = DES.new(key, DES.MODE_CBC)

r = cipher.iv
f = cipher.encrypt(pad(plain, 8, "x923"))

print(f.hex())
print(r.hex())


#----------------------------------------------------------------------------------#
print("")
#----------------------------------------------------------------------------------#


# AES256

key = Random.get_random_bytes(32)
print(key.hex())

plain = "Mi chiedo cosa significhi il numero nel nome di questo algoritmo.".encode("utf-8")
chiper = AES.new(key, AES.MODE_CFB, segment_size=24)

r = chiper.iv
f = chiper.encrypt(pad(plain, 16, "pkcs7"))

print(f.hex())
print(r.hex())


#----------------------------------------------------------------------------------#
print("")
#----------------------------------------------------------------------------------#


# ChaCha20

key = bytes.fromhex("4c79e996477d864c3ace0fa8f6e0afca4ba4d3d1ec4e72331abc86d05e0fd8ee")
chiper = bytes.fromhex("e51f7c6f51e95f619e8d43d0390021d471499e6ca5a6062211d2c9c8")
nonce = bytes.fromhex("b6f1c7ce3e17947e")

plain = ChaCha20.new(key=key, nonce=nonce)

f = plain.decrypt(chiper)

print(f.decode())