#!/usr/bin/env python3

import os
import signal
from Crypto.Cipher import AES
from Crypto.Random.random import randint, shuffle
from Crypto.Util.Padding import pad
from secret import aes_key, secret_int

TIMEOUT = 300

assert("FLAG" in os.environ)
flag = os.environ["FLAG"]
assert(flag.startswith("flag{"))
assert(flag.endswith("}"))

def handle():
    print('Benvenuto nel Super Miscelatore Entropico!')
    print('Questo servizio fa uso di due sorgenti di entropia (hardware ed umana).')
    print('Queste vengono poi combinate per ottenere una sicurezza astrale!')

    entropia_umana = input('\nIn attesa di ricezione di entropia umana. Premi qualche tasto a caso ed invia! ').encode()
    entropia_hardware = os.urandom(AES.block_size)

    msgs = [entropia_umana.hex(), entropia_hardware.hex(), flag.encode().hex()]
    merge = AES.new(aes_key, AES.MODE_ECB).encrypt(pad(entropia_umana + entropia_hardware, AES.block_size))
    shuffle(msgs)

    print('Ciphertext:', AES.new(aes_key, AES.MODE_CTR, nonce=merge[:secret_int]).encrypt(''.join(msgs).encode()).hex())
    print('Grazie per aver usato il Super Miscelatore Entropico, alla prossima!')
    return



if __name__ == "__main__":
    signal.alarm(TIMEOUT)
    handle()
