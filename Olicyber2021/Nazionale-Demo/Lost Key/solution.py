import ctypes

libc = ctypes.CDLL(None)

libc.srand(0)

ctx = [[0] * 4 for _ in range(11 * 4)] 
key = [[0] * 4 for _ in range(4)]

with open("ciphertext.txt", "r") as f:
    flag = [int(x) for x in f.read().split()]

sbox = [99, 124, 119, 123, 242, 107, 111, 197,  48,   1,
        103,  43, 254, 215, 171, 118, 202, 130, 201, 125,
        250,  89,  71, 240, 173, 212, 162, 175, 156, 164,
        114, 192, 183, 253, 147,  38,  54,  63, 247, 204,
         52, 165, 229, 241, 113, 216,  49,  21,   4, 199,
         35, 195,  24, 150,   5, 154,   7,  18, 128, 226,
        235,  39, 178, 117,   9, 131,  44,  26,  27, 110,
         90, 160,  82,  59, 214, 179,  41, 227,  47, 132,
         83, 209,   0, 237,  32, 252, 177,  91, 106, 203,
        190,  57,  74,  76,  88, 207, 208, 239, 170, 251,
         67,  77,  51, 133,  69, 249,   2, 127,  80,  60,
        159, 168,  81, 163,  64, 143, 146, 157,  56, 245,
        188, 182, 218,  33,  16, 255, 243, 210, 205,  12,
         19, 236,  95, 151,  68,  23, 196, 167, 126,  61,
        100,  93,  25, 115,  96, 129,  79, 220,  34,  42,
        144, 136,  70, 238, 184,  20, 222,  94,  11, 219,
        224,  50,  58,  10,  73,   6,  36,  92, 194, 211,
        172,  98, 145, 149, 228, 121, 231, 200,  55, 109,
        141, 213,  78, 169, 108,  86, 244, 234, 101, 122,
        174,   8, 186, 120,  37,  46,  28, 166, 180, 198,
        232, 221, 116,  31,  75, 189, 139, 138, 112,  62,
        181, 102,  72,   3, 246,  14,  97,  53,  87, 185,
        134, 193,  29, 158, 225, 248, 152,  17, 105, 217,
        142, 148, 155,  30, 135, 233, 206,  85,  40, 223,
        140, 161, 137,  13, 191, 230,  66, 104,  65, 153,
         45,  15, 176,  84, 187,  22]

rsbox = [82,   9, 106, 213,  48,  54, 165,  56, 191,  64,
        163, 158, 129, 243, 215, 251, 124, 227,  57, 130,
        155,  47, 255, 135,  52, 142,  67,  68, 196, 222,
        233, 203,  84, 123, 148,  50, 166, 194,  35,  61,
        238,  76, 149,  11,  66, 250, 195,  78,   8,  46,
        161, 102,  40, 217,  36, 178, 118,  91, 162,  73,
        109, 139, 209,  37, 114, 248, 246, 100, 134, 104,
        152,  22, 212, 164,  92, 204,  93, 101, 182, 146,
        108, 112,  72,  80, 253, 237, 185, 218,  94,  21,
         70,  87, 167, 141, 157, 132, 144, 216, 171,   0,
        140, 188, 211,  10, 247, 228,  88,   5, 184, 179,
         69,   6, 208,  44,  30, 143, 202,  63,  15,   2,
        193, 175, 189,   3,   1,  19, 138, 107,  58, 145,
         17,  65,  79, 103, 220, 234, 151, 242, 207, 206,
        240, 180, 230, 115, 150, 172, 116,  34, 231, 173,
         53, 133, 226, 249,  55, 232,  28, 117, 223, 110,
         71, 241,  26, 113,  29,  41, 197, 137, 111, 183,
         98,  14, 170,  24, 190,  27, 252,  86,  62,  75,
        198, 210, 121,  32, 154, 219, 192, 254, 120, 205,
         90, 244,  31, 221, 168,  51, 136,   7, 199,  49,
        177,  18,  16,  89,  39, 128, 236,  95,  96,  81,
        127, 169,  25, 181,  74,  13,  45, 229, 122, 159,
        147, 201, 156, 239, 160, 224,  59,  77, 174,  42,
        245, 176, 200, 235, 187,  60, 131,  83, 153,  97,
         23,  43,   4, 126, 186, 119, 214,  38, 225, 105,
         20,  99,  85,  33,  12, 125, 141,   1,   2,   4,
          8,  16,  32,  64, 128,  27,  54,   0,   0,   0,
          0,   0]

Rcon = [141, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54, 0, 0, 0, 0, 0]

for i in range(4):
    n = libc.rand()
    for j in range(4):
        key[i][j] = n % 256
        n >>= 8

for i in range(4):
    for j in range(4):  
        ctx[i][j] = key[i][j]

for j in range(4, 44):
    prev  = j - 1 
    prev4 = j - 4 

    n0 = ctx[prev][0]
    n1 = ctx[prev][1]
    n2 = ctx[prev][2]
    n3 = ctx[prev][3]

    if j % 4 == 0:
        n0, n1, n2, n3 = (
            sbox[n1] ^ Rcon[j // 4],
            sbox[n2],
            sbox[n3],
            sbox[n0],
        )

    r = j

    ctx[r][0] = ctx[prev4][0] ^ n0
    ctx[r][1] = ctx[prev4][1] ^ n1
    ctx[r][2] = ctx[prev4][2] ^ n2
    ctx[r][3] = ctx[prev4][3] ^ n3


def AggiungiChiaveDiRound(round_idx, state, ctx):
    base = round_idx * 4 
    for i in range(4): 
        for j in range(4): 
            state[4 * i + j] ^= ctx[base + i][j]


def funzione2Inversa(state):
    v2 = state[13]
    state[13] = state[9]
    state[9] = state[5]
    state[5] = state[1]
    state[1] = v2
    v3 = state[2]
    state[2] = state[10]
    state[10] = v3
    v4 = state[6]
    state[6] = state[14]
    state[14] = v4
    v5 = state[3]
    state[3] = state[7]
    state[7] = state[11]
    state[11] = state[15]
    state[15] = v5


def funzione1Inversa(state):
    for j in range(4):
        for i in range(4):
            state[i + 4 * j] = rsbox[state[i + 4 * j]]


def xtime(a):
    return ((a << 1) ^ 0x1B) & 0xFF if a & 0x80 else (a << 1) & 0xFF


def Moltiplica(a, b):
    res = 0
    for _ in range(8):
        if b & 1:
            res ^= a
        a = xtime(a)
        b >>= 1
    return res


def funzione3Inversa(state):
    for i in range(4):
        a0, a1, a2, a3 = state[4*i:4*i+4]
        state[4*i+0] = Moltiplica(a0,14) ^ Moltiplica(a1,11) ^ Moltiplica(a2,13) ^ Moltiplica(a3, 9)
        state[4*i+1] = Moltiplica(a0, 9) ^ Moltiplica(a1,14) ^ Moltiplica(a2,11) ^ Moltiplica(a3,13)
        state[4*i+2] = Moltiplica(a0,13) ^ Moltiplica(a1, 9) ^ Moltiplica(a2,14) ^ Moltiplica(a3,11)
        state[4*i+3] = Moltiplica(a0,11) ^ Moltiplica(a1,13) ^ Moltiplica(a2, 9) ^ Moltiplica(a3,14)


def decrypt(state, ctx):
    AggiungiChiaveDiRound(10, state, ctx)

    for i in range(9, -1, -1):
        funzione2Inversa(state)
        funzione1Inversa(state)
        AggiungiChiaveDiRound(i, state, ctx)
        if i != 0:
            funzione3Inversa(state)


decrypt(flag, ctx)

for c in flag:
    print(chr(c), end="")
print()