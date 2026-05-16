import pyshark

cap = pyshark.FileCapture("capture.pcapng")

fp = open("output", "wb")

for packet in cap:
    if hasattr(packet, "dns"):
        data = packet.dns._all_fields["dns.resp.name"]
        if "attacker.eve" in data:
            data = data.split(".")

            hex_data = data[1]

            try:
                flag = bytes.fromhex(hex_data)
                
                fp.write(flag)
            except Exception:
                continue