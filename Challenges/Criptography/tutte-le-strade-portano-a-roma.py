flag = list("cixd{xsb_zxbpxo_jlofqrof_qb_pxirqxkq}")

shift = ord('f')-ord('c')

for l in flag:
    if l == '{' or l == '}' or l == '_':
        print(l, end="")
    else:        
        diff = ord(l) + shift
        if diff > ord('z'):
            diff -= 26

        print(chr(diff), end="")

print()