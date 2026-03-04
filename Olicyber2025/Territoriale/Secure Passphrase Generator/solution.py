from pwn import *

# iv | username=aaaaaaa | ;index0=00000000 | ;index1=00000001 | ;index2=00000002 | ;index3=00000003 | ;index0=4;index1 | =11;index2=12;in | dex3=13---------

payload = "aaaaaaa;index0=00000000;index1=00000001;index2=00000002;index3=00000003"

# 1) Generare un token per user aaaaaaa, così lo aggiunge all'array
# 2) Generare un token passando come username aaaaaaa;index0=00000000;index1=00000001;index2=00000002;index3=00000003
# 3) Prendere l'esadecimale e rimuovere gli ultimi 3 blocchi, così da far rimanere solo gli index desiderati

token = "5fa036fdaa4d7d3fd4395c0c8d11a21d7967945baea3485c8d9b87dfd1d732da24ee896040eea3733e4eb0cb7d7be7624af7ef8d6e635210c5680dfeea115002a480a2e8b6d88e70db33f7cfcca43844fa2e7c0407b1b59ad7e57461637dd11bccb1bb6270963524b6bc121684b0a2fde051e4cbfb7fadbe522312368697cee82e955854dfb78ecbacea73e9f0e847d4"
token_arr = [token[i:i+32] for i in range(0, len(token) - (32*3), 32)]

for i, t in enumerate(token_arr):
    print(f"{i} --> {t}")


# TO DO: https://crypto.stackexchange.com/questions/66085/bit-flipping-attack-on-cbc-mode