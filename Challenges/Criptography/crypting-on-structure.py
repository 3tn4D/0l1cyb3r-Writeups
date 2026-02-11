flag = list("AAAABAAAAAAAABAABBBAABBABABAAABAABABAABAABBBABAABBAAAAABAABABAABBBBAAA")
bin_flag = ""

for c in flag:
    if c == 'A': bin_flag += '0'
    else: bin_flag += '1'

print("flag{", end="")
for i in range(0, 70, 5):
    letter = int(bin_flag[i:i+5], 2)
    print(chr(letter + ord('A')), end="")

print("}")