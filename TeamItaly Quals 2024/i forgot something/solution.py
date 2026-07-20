def decode_file(input_path, output_path):
    with open(input_path, "rb") as f:
        data = bytearray(f.read())

    key = b"\xD0\xD0\xAD\xDE\xEF\xBE\xAD\xDE"
    curr = 0
    key_idx = 0

    while curr < len(data):
        if key_idx != 8:
            kb = key_idx
            key_idx += 1

            data[curr] ^= key[kb]
            curr += 1
        else:
            data[curr] ^= 0xD0
            curr += 1
            key_idx = 1

    with open(output_path, "wb") as f:
        f.write(data)


decode_file("forgot", "forgot_dec") # Use this to rev the functions (you can also do it in another way XD)

def decode(text, key):
    text = list(text)

    key_pos = 0
    key_len = len(key)

    for i in range(len(text)):
        c = text[i]

        if key_pos < key_len:
            key_idx = key_pos
            key_pos += 1
        else:
            key_pos = 1
            key_idx = 0

        if 'a' <= c <= 'z':
            text[i] = chr(
                (ord(c) - ord(key[key_idx]) + 26) % 26 + ord('a')
            )

    return ''.join(text)


raw_flag = "TAqNxPfTINsTpMoXyY{UhOqKzMkLrWsV_NiXoMsW_QdVbIoIiIhIcFjQ:KeMdE_PkNhKgS_SgPhEvV_Q8A4E2M9V2W3RuF7T}J"

cipher = raw_flag[::2]

key = "fezpnrfbaj"

for _ in range(3):
    cipher = decode(cipher, key)

print(cipher)