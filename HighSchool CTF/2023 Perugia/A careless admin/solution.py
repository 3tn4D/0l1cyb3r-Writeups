import pyshark
from base64 import b64decode

cap = pyshark.FileCapture("A careless admin.pcapng")
for packet in cap:
    if "HTTP" in str(packet):
        http_layer = packet.http

        if hasattr(http_layer, "file_data"):
            hex_data = http_layer.file_data.replace(":", "")
            data = bytes.fromhex(hex_data).decode()
            
            if "success" in data:
                flag = data.split("The flag is ")[1][:-1]

                flag = b64decode(flag).decode()
                print(flag)