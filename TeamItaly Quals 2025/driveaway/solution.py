from pwn import *
import ctypes
import time
from multiprocessing import Pool

libc = ctypes.CDLL("libc.so.6")

ASCII = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$^&*()_+[]{}|;\':,.<>?/`~'

def srand(seed):
    libc.srand(ctypes.c_uint(seed))

def rand():
    return libc.rand()

def get_rand_char():
    r = rand()
    return ord(ASCII[r % len(ASCII)])

class Node:
    def __init__(self, chr_val):
        self.chr = chr_val
        self.left = None
        self.right = None
        self.left_weight = 0
        self.right_weight = 0

def build_tree(seed):
    srand(seed)
    all_nodes = []
    current_level = []
    next_level = []

    root = Node(get_rand_char())
    current_level.append(root)
    all_nodes.append(root)

    for i in range(16):
        src = current_level if i % 2 == 0 else next_level
        dst = next_level   if i % 2 == 0 else current_level

        while src:
            front = src.pop(0)
            if not front:
                break

            new_node = Node(get_rand_char())
            rand_n_1 = rand()
            front.left = new_node
            front.left_weight = rand_n_1 % 20

            new_node_1 = Node(get_rand_char())
            rand_n_2 = rand()
            front.right = new_node_1
            front.right_weight = rand_n_2 % 20

            dst.append(new_node)
            all_nodes.append(new_node)
            dst.append(new_node_1)
            all_nodes.append(new_node_1)

    return root, all_nodes

def swap_weights(node):
    node.left_weight, node.right_weight = node.right_weight, node.left_weight

def gen_string(node):
    path = []
    curr = node
    while curr:
        path.append(chr(curr.chr))
        if curr.left and curr.right:
            curr = curr.left if curr.left_weight < curr.right_weight else curr.right
        elif curr.left:
            curr = curr.left
        else:
            curr = curr.right
    return ''.join(path)

def find_swaps(root, all_nodes, target):
    node_to_idx = {id(n): i for i, n in enumerate(all_nodes)}
    swaps = []
    curr = root
    target_idx = 0

    while curr and target_idx < len(target):
        if curr.left and curr.right:
            goes_left = curr.left_weight < curr.right_weight
            need_left = chr(curr.left.chr) == target[target_idx + 1] if target_idx + 1 < len(target) else False

            if goes_left != need_left:
                swaps.append(node_to_idx[id(curr)])
                swap_weights(curr)

            curr = curr.left if curr.left_weight < curr.right_weight else curr.right

        elif curr.left:
            curr = curr.left
        else:
            curr = curr.right

        target_idx += 1

    return swaps

def try_range(args):
    ts, r_start, r_end, target = args
    libc = ctypes.CDLL("libc.so.6")

    def srand(seed):
        libc.srand(ctypes.c_uint(seed))

    def rand():
        return libc.rand()

    def get_rand_char():
        r = rand()
        return ord(ASCII[r % len(ASCII)])

    for r in range(r_start, r_end):
        seed = ts ^ r
        root, all_nodes = build_tree(seed)
        original = gen_string(root)

        if original == target:
            for j in range(32768):
                rand_n_3 = rand()
                random_node = all_nodes[rand_n_3 % len(all_nodes)]
                swap_weights(random_node)
            return seed, ts, r, root, all_nodes, original

    return None

def bruteforce(target, timestamp):
    from multiprocessing import cpu_count
    ncores = cpu_count()
    chunk = 2000 // ncores

    tasks = []
    for ts in range(timestamp - 10, timestamp + 10):
        for i in range(ncores):
            r_start = i * chunk
            r_end = r_start + chunk if i < ncores - 1 else 2000
            tasks.append((ts, r_start, r_end, target))

    total = len(tasks)
    done = 0
    print(f"[*] bruteforcing with {ncores} cores, {total} tasks")

    with Pool() as pool:
        for result in pool.imap_unordered(try_range, tasks):
            done += 1
            if done % 10 == 0:
                print(f"[*] {done}/{total} tasks done", end='\r')
            if result:
                seed, ts, r, root, all_nodes, original = result
                print(f"\n[+] found seed: {seed} (ts={ts}, r={r})")
                pool.terminate()
                return root, all_nodes, original

    print("\n[-] seed not found")
    return None, None, None


io = remote("driveway.challs.olicyber.it", 38078)

io.recvuntil(b"This is your driveway, can you follow it?\n")
target = io.recvline().strip().decode()
now = int(time.time())
print(f"[+] target: {target}")
io.recvuntil(b"Let's start the game!\n")

# bruteforce
root, all_nodes, original = bruteforce(target, now)
if not root:
    print("[-] seed not found")
    exit()

# verify locally
result = gen_string(root)
print(f"[+] after swaps gen_string: {result}")
print(f"[+] target:                 {original}")
print(f"[+] local match: {result == original}")

# figure out which nodes to swap
swaps = find_swaps(root, all_nodes, original)
print(f"[+] swaps needed: {swaps}")

# verify after find_swaps
result2 = gen_string(root)
print(f"[+] after find_swaps gen_string: {result2}")
print(f"[+] match: {result2 == original}")

# send swaps
for idx in swaps:
    io.sendline(f"{idx} HONDA CIVIC".encode())
    print(f"[*] sent swap {idx}")

# trigger
io.sendline(b"TOYOTA COROLLA")
print("[*] sent TOYOTA COROLLA")

io.interactive()