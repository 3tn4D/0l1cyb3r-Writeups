flag_enc = "fmcj{yo_ackyzb_ihruvcvjam}"
flag_dec = ""

spec = "{}_"

for i, c in enumerate(flag_enc):
    if c not in spec:    
        flag_dec += chr(((ord(c) - 97 - i) % 26) + 97)
    else:
        flag_dec += c

print(flag_dec)