#!/usr/bin/env python3

import os
import struct
import math
import random
from Crypto.Util.Padding import pad
from Crypto.Util.number import long_to_bytes

class Hash:
    def __init__(self, init_state: int):
        self.BLOCK_SIZE = 8
        self.DIGEST_SIZE = 16
        self.init_state = init_state
        self.c = int.from_bytes(struct.pack('<d', math.e)*((self.DIGEST_SIZE + self.BLOCK_SIZE)//8), 'big')
        random.seed(0x1337)
        self.bit_perm = list(range(8*(self.DIGEST_SIZE + self.BLOCK_SIZE)))
        random.shuffle(self.bit_perm)

    def F(self, a, b, bitsize):
        for r in range(bitsize):
            bit = (b >> r) & 1
            tmp = 0

            for i, bit_index in enumerate(self.bit_perm):
                new_bit = (a >> (bit_index ^ bit)) & 1
                tmp |= (new_bit << i)

            a = tmp ^ self.c
        
        return a

    def h(self, m):
        if type(m) == int:
            m = long_to_bytes(m)
        m = pad(m, self.BLOCK_SIZE)
        state = self.init_state

        blocks = [int.from_bytes(m[i:i+self.BLOCK_SIZE], 'big') for i in range(0, len(m), self.BLOCK_SIZE)]

        for b in blocks:
            tmp = self.F((state << (8*self.BLOCK_SIZE)) + b, b, 8*self.BLOCK_SIZE)
            state = self.F((state << (8*self.BLOCK_SIZE)) + b, tmp, 8*(self.BLOCK_SIZE + self.DIGEST_SIZE))
            state = state ^ tmp
            state = state >> (8*self.BLOCK_SIZE)
        
        return state