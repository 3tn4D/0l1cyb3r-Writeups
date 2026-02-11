from base64 import b64decode

s = "ZmxhZ3t3NDF0XzF0c19hbGxfYjE="
i = 664813035583918006462745898431981286737635929725

s = b64decode(s)
i = i.to_bytes(len(str(i)), 'big')

print((s + i).decode())