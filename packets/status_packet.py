import json
from packets.packet import Packet

from utils import toaddr, known_addresses

class StatusPacket(Packet):
    @staticmethod
    def can_parse(b: bytearray) -> bool:
        addr1 = toaddr(b, 3, 4, 5, 6)
        addr2 = toaddr(b, 7, 8, 9, 10)
        addr3 = toaddr(b, 11, 12, 13, 14)
        if addr1 is not None and addr1 not in known_addresses:
            return False
        if addr2 is not None and addr2 not in known_addresses:
            return False
        if addr3 is not None and addr3 not in known_addresses:
            return False
        if not (10 < (b[24] * 256 + b[23]) / 128.0 < 60):
            return False
        return True

    @property
    def temperature(self) -> float:
        return (self._bytes[24] * 256 + self._bytes[23]) / 128.0

    @property
    def seconds_on(self) -> int:
        return self._bytes[26]

    @staticmethod
    def known_fields() -> list[int]:
        return [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 23, 24, 26]

    def from_addr(self) -> str:
        return self.addr3 if self.addr3 else self.addr2

    def to_json(self) -> str:
        return json.dumps({
            "from": self.from_addr(),
            "type": "status",
            "temperature": self.temperature,
            "seconds_on": self.seconds_on})

    def __str__(self) -> str:
        return f"{self.receiver:>8}:  Status: {self.addr1:>8}, {str(self.addr2):>8}, {str(self.addr3):>8}: {self.temperature}°C, {self.seconds_on} seconds on, {self.unknown()}"
