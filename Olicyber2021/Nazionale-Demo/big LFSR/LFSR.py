import random
from secret import flag

def xor(a, b):
    return bytes([x^y for x,y in zip(a,b)])

class LFSR(object):
    def __init__(self, s):
        self.s = list(map(int, s))

    def gen_stream(self, n):
        out = []
        for i in range(n):
            out.append(self.s[0]^self.s[12]^self.s[21]^self.s[34]^self.s[50])
            self.s = self.s[1:] + [self.s[0]^self.s[3]^self.s[7]^self.s[9]]
        return out

initial_state = random.randint(0,2**56) # 2**56 = 72057594037927936, impossible to bruteforce!
initial_state = [int(x) for x in bin(initial_state)[2:].rjust(56, '0')]
L = LFSR(initial_state)

k = b""

for i in range(len(flag)):
    k += bytes([int("".join(str(x) for x in L.gen_stream(8)), 2)])

print(xor(flag, k).hex())
