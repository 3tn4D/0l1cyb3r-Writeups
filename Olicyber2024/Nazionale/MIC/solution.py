from pwn import *

logging.disable()
r = process("./MIC")

grille = [["" for _ in range(6)] for _ in range(6)]
secret = [[0,1],[1,1],[1,3],[3,1],[3,3],[4,5],[5,0],[5,2],[5,3]]
encrypted_key = "SP3CCSPXE6ZUC2HC9HJLDZX52UN5H8AO5WDZ"

def format_key(buf):
    for i in range(6):
        for j in range(6):
            grille[i][j] = buf[j + i * 6]

def rotate_grille():
    tmp = [''] * 36
    c = 0
    for i in range(6):
        for j in range(5, -1, -1):
            tmp[c] = grille[j][i]
            c += 1
    format_key(tmp)

def unrotate_grille():
    for _ in range(3):
        rotate_grille()

format_key([""] * 36)

for _ in range(4):
    rotate_grille()

for i in range(3, -1, -1):
    unrotate_grille()
    for j in range(9):
        grille[secret[j][0]][secret[j][1]] = encrypted_key[i * 9 + j]

key = ""
for i in range(6):
    for j in range(6):
        key += grille[i][j]

r.recv(1000)
r.sendline(key.encode())
r.recvline()
print(r.recvline().decode().strip())