known_addresses = {
    "abd200a8": "Soverom",
    "b7d200a8": "Kjøkken",
    "9bd200a8": "Stue",
    "e07e0066": "Hub",
}

theories = {25: "#s on"}

def crc16(data: bytearray, offset: int, length: int) -> int:
    if (
        data is None
        or offset < 0
        or offset > len(data) - 1
        and offset + length > len(data)
    ):
        return 0
    crc = 0xFFFF
    for i in range(0, length):
        crc ^= data[offset + i] << 8
        for j in range(0, 8):
            if (crc & 0x8000) > 0:
                crc = (crc << 1) ^ 0x1021
            else:
                crc = crc << 1
    return crc & 0xFFFF



def toaddr(data: bytearray, *args: int) -> str | None:
    hexes = reversed([hex(data[i])[2:] for i in args])
    data = "".join(["00" if a == "0" else a for a in hexes])
    return None if data == "00000000" else data
