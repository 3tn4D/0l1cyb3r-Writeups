#!/usr/bin/env python3
import hashlib
import sys

target = sys.argv[1]

i = 0
while True:
    h = hashlib.sha1(str(i).encode('ascii')).hexdigest()
    if h.endswith(target):
        print(i)
        break

    i += 1

# find / -type f -print0 | xargs -0 grep -H "flag{"

# flag{l1nux_15_4_c0mpl3x_And_4m4Z1ng_cr34Tur3}
