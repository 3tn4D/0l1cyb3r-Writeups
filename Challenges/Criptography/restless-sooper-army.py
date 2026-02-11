from Cryptodome.Cipher import AES

# -------- RSA --------
p = 27124318089513964313
q = 30114955579980689081
e = 65537

n = p * q
print("n: " + str(n))

phi_n = (p - 1) * (q - 1)
print("Phi(n): " + str(phi_n))

d = pow(e, -1, phi_n)
print("d: "+ str(d))

msg = int.from_bytes("Rivest".encode(), "big")
c = pow(msg, e, n)
print("c: " + str(c))

print("\n")

# -------- AES_CBC --------
iv = bytes.fromhex("27b85b41ad0d9722e043c0b7730265a2")
key = int("23aa205f1322ad71d3acf1ed721f28d2f", 16)
token = bytes.fromhex("571c1dda7c957ddf27f9b829bddf0edde64b7404442667f890d14500c531d96a")

key = pow(key, d, n)
key = bytes.fromhex(hex(key)[2:])

chiper = AES.new(key, AES.MODE_CBC, iv)

flag = chiper.decrypt(token)
print(flag.decode().strip())