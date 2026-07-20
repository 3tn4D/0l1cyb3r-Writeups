MEM = bytearray([42, 57, 103, 126, 113, 45, 33, 33, 114, 67, 65, 58, 9, 12, 4, 5, 82, 66, 64, 25, 10, 119, 81, 66, 5, 35, 54, 91, 12, 103, 102, 34, 0, 75, 39, 56, 71, 114, 110, 91, 117, 43, 44, 50, 94, 83, 71, 90, 34, 112, 116, 109, 123, 0, 119, 104, 97, 116, 39, 115, 32, 116, 104, 105, 115, 63, 0, 122, 122, 122, 46, 46, 46, 0, 0, 0, 0, 0, 0, 0, 116, 104, 120, 32, 46, 46, 46, 122, 122, 122, 122, 122, 122, 46, 46, 46, 0, 42])

flag_idx = 0
prev = 0x2a

def review(p):
    global flag_idx, prev
    flag_idx += 1
    prev = MEM[flag_idx] ^ p ^ prev
    
    # check if flag starts with ptm{
    if flag_idx <= 4 and prev == MEM[49 + flag_idx - 1]:
        return 'zzz...'
    else:
        if prev < 128: # check if it's an ascii
            if flag_idx == 47 and prev == ord('}'): 
                return 'thx ...zzzzzz...'
            elif flag_idx < 47:
                return 'zzz...'
        else:
            return "what's this?"

sol = ["c", "c", "g", "g", "a", "a", "g", "-", "f", "f", "e", "e", "d", "d", "c", "-", "g", "g", "f", "f", "e", "e", "d", "-", "g", "g", "f", "f", "e", "e", "d", "-", "c", "c", "g", "g", "a", "a", "g", "-", "f", "f", "e", "e", "d", "d", "c", "-"]

for note in sol:
    review(ord(note))
    print (chr(prev), end='')
print()