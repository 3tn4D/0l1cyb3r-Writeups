import random
import string

# f = x
# l = c
# a = q
# g = v
encypted_flag = "xcqv{gvyavn_zvztv_etvtddlnxcgy}"
alphabet = "abcdefghijklmnopqrstuvwxyz"


def decrypt(chipertext, key):
    plain = ""
    for k in range(len(chipertext)):
        character = chipertext[k]

        if character in alphabet:
            i = key.index(character)
            characterDecrypted = alphabet[i]

            key = key[-1] + key[:-1]

            plain += characterDecrypted
        else:
            plain += character
    
    return plain


    
key = "stuvwxyzabcdefghijklmnopqr"
plaintextFLAG = decrypt(encypted_flag, key)

print(plaintextFLAG)