def xor(a, b):
    return bytes([x^y for x,y in zip(a,b)])

class LFSR(object):
    def __init__(self, s):
        self.s = list(map(int, s))

    def gen_stream(self, n):
        out = []
        for i in range(n):
            out.append(self.s[0])
            self.s = self.s[1:] + [self.s[0]^self.s[3]^self.s[7]^self.s[9]]
        return out

ciphertext = bytes.fromhex(open("data.txt", "r").read())

known = b"flag{"
keystream = xor(ciphertext[:len(known)], known)

# 40 bits of s, missing 16 bit
known_bits = []
for i, byte in enumerate(keystream):
    bits = [int(x) for x in bin(byte)[2:].rjust(8, '0')]
    known_bits += bits

# bruteforce the last 16 bits
for guess in range(2**16):
    missing_bits = [int(x) for x in bin(guess)[2:].rjust(16, "0")]

    state = known_bits + missing_bits

    L = LFSR(state)

    k = b""
    for i in range(len(ciphertext)):
        k += bytes([int("".join(str(x) for x in L.gen_stream(8)), 2)])
    
    plaintext = xor(ciphertext, k)

    if plaintext.endswith(b"}") and all(32 <= c < 127 for c in plaintext):
        print(plaintext.decode())