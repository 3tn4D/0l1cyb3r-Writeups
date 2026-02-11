def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def is_printable(s: bytes):
    return all(32 <= val <= 126 for val in s)

flag = bytes.fromhex("104e137f425954137f74107f525511457f5468134d7f146c4c")

# key is 1 byte
for key in range(2 ** 8):
    curr = xor(flag, bytes([key]) * len(flag))

    if(is_printable(curr)):
        print("flag{" + curr.decode() + "}")
        break