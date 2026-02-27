from base64 import b64decode, b64encode
from Cryptodome.Cipher import AES

# |nome_random|;pts=0000000001|

def xor(a, b):
    return bytes(x^y for x, y in zip(a, b))

start = ";pts=0000000000".encode()
target = ";pts=1000000000".encode()

token = b64decode("y5Ddg/Op5DeCT/5sxhZT66xamEeGZLGseKrZSfIODBM=")
blocks = [token[:16], token[16:]]

new_block = [
    xor(xor(blocks[0], blocks[1]), start),
    blocks[1]
]

print(b64encode(b"".join(new_block)).decode())