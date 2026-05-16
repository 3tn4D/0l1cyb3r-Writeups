from pwn import *
from collections import deque

def solve(stato, mosse):
    target = 5
    stato_iniziale = tuple(stato)
    
    # BFS: ogni nodo è (stato_corrente, sequenza_mosse_usate)
    queue = deque()
    queue.append((stato_iniziale, []))
    visited = set()
    visited.add(stato_iniziale)
    
    while queue:
        curr_stato, curr_mosse = queue.popleft()

        # Condizione di vittoria: tutti i contatori >= 5
        if all(v == 5 for v in curr_stato):
            return " ".join(str(m) for m in curr_mosse)
        
        # Prova ogni pulsante (1-indexed nell'output)
        for i, mossa in enumerate(mosse):
            nuovo_stato = list(curr_stato)
            for bottone in mossa:
                nuovo_stato[bottone] += 1
                if nuovo_stato[bottone] > 5:
                    nuovo_stato[bottone] = 1
            nuovo_stato = tuple(nuovo_stato)
            
            if nuovo_stato not in visited:
                visited.add(nuovo_stato)
                queue.append((nuovo_stato, curr_mosse + [i + 1]))
    
    return ""  # non dovrebbe mai arrivare qui

r = remote("test2.challs.olicyber.it", 15005)
context.log_level = 'debug'
r.recvlines(20)

livello = r.recvline()
while livello.startswith(b"Livello"):
    stato = [int(_) for _ in r.recvline(False).decode().split()]
    mosse = []
    while True:
        s = r.recvline(False).decode()
        if s == "":
            break
        mosse.append(["ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(_) for _ in s.split()])
    res = solve(stato, mosse)
    r.sendline(res)
    r.recvlines(2)
    livello = r.recvline()


# 1 -> C
# 2 -> A B
# 3 -> D

# A B C D
# 3 3 5 4

# 4 4 5 4   <- 2
# 5 5 5 4   <- 2
# 5 5 5 5   <- 3

