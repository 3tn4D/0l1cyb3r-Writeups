import os
from hashlib import sha256
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad

CHUNK_SIZE = 13337
iv = b'\x00' * 16
directory = "encrypted_chunks"

files = []
for file_to_encrypt in os.listdir(directory):
    files.append(file_to_encrypt)
files.sort()

result = [[] for _ in range(5)]

idx = 0
for chunk in files:
    key_name = chunk.split("_")[0]
    idx = int(chunk[8])

    with open(f"{directory}/{chunk}", "rb") as f:
        encrypted_data = f.read()
    
    cipher = AES.new(sha256(key_name.encode()).digest(), AES.MODE_CBC, iv)
    dec = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    result[idx].append(dec)

for i, chunks in enumerate(result):
    content = b"".join(chunks)
    with open(f"output{i}.png", "wb") as f:
        f.write(content)