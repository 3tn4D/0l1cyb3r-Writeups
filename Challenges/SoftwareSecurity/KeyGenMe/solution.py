from pwn import *

def makeSerial(userid):
    output = [''] * 54
    pairStrings(output, 0, userid, 18, userid, 9, 8)
    pairStrings(output, 16, userid, 0, userid, 18, 8)
    pairStrings(output, 32, userid, 9, userid, 0, 8)
    output[48] = '\0'
    return ''.join(output)

def pairStrings(output, out_offset, src1, pos1, src2, pos2, n):
    local_14 = 0
    local_10 = 0
    local_c = 0
    while (local_10 < n) or (local_c < n):
        if (local_14 & 1) == 0:
            output[out_offset + local_14] = src1[pos1 + local_10]
            local_10 += 1
        else:
            output[out_offset + local_14] = src2[pos2 + local_c]
            local_c += 1
        local_14 += 1

r = remote("keygenme.challs.olicyber.it", 10017)

userid = r.recvline().decode().split(":")[1].strip()

r.recv(512)

output = makeSerial(userid)
r.sendline(output.encode())

print(r.recv(512).decode())