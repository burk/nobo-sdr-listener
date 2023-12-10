from __future__ import annotations
import sys
from packets.packet import Packet, CRCError, ParseError

df = []
for line in sys.stdin:
    tokens = line.split(",")
    timestamp = tokens[0]
    data = tokens[2][5:]
    try:
        packet = Packet.from_hex(data)
    except (CRCError, ParseError):
        continue
    print(packet)
