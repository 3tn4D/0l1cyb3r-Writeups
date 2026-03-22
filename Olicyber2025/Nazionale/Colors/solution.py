from PIL import Image
import numpy as np
from hashlib import sha256
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

ciphertext_hex = open("colors_output/ciphertext.txt", "r").readline().strip()
ct = bytes.fromhex(ciphertext_hex)
iv, ct = ct[:16], ct[16:]

# Estrai i colori dai pixel NON bianchi delle immagini
def get_color(path):
    n = np.array(Image.open(path).convert('RGBA'))
    # Prendi il primo pixel non-bianco
    mask = ~(n[:, :, 0:4] == [255, 255, 255, 255]).all(2)
    return n[mask][0][:4].tolist()

g_col = get_color('colors_output/g.png')
A_col = get_color('colors_output/A.png')
B_col = get_color('colors_output/B.png')

# Recupera la chiave privata 'a'
a = [(A - g) % 256 for A, g in zip(A_col, g_col)]

# Calcola il segreto condiviso: shared = mix(B, a) = B + a mod 256
shared = [(b_c + a_c) % 256 for b_c, a_c in zip(B_col, a)]

# Decifra
key = sha256(bytes(shared)).digest()
cipher = AES.new(key, AES.MODE_CBC, iv)
flag = unpad(cipher.decrypt(ct), 16)
print(flag.decode())