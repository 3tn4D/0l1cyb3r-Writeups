import pyshark

cap = pyshark.FileCapture("llt.pcap", display_filter="icmp")
for packet in cap:
    src = str(packet.ip.src)
    dst = str(packet.ip.dst)
    if src == "172.19.0.2" and dst == "172.67.157.96":
        print(chr(int(packet.ip.ttl)), end="")
    
print()