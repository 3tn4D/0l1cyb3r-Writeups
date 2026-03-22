import pyshark
import json

f = open("out_key.txt", "w")

cap = pyshark.FileCapture("keylogger.pcap")
for packet in cap:
        if str(packet.usb.src) == "2.3.2":
            hid_key = packet.data._all_fields['usb.capdata']
            f.write(hid_key + "\n")

# Quando lo finisce mandalo a claude e fattelo decodificare
# ( se lo fai a mano sei un pazzo )