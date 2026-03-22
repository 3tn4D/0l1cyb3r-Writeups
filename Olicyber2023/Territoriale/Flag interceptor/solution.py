import pyshark

cap = pyshark.FileCapture("./flag-interceptor.pcap")


flag = {}
for packet in cap:
    if "DATA" in str(packet.layers):
        c = chr(int(packet.data.data[:-2], 16))
        src = str(packet.ip.src)

        if src not in flag:
            flag[src] = ""

        flag[src] += c
        
for ip, msg in flag.items():
    if msg.startswith("flag{") and msg.endswith("}"):
        print(msg)