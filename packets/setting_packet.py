from utils import toaddr, known_addresses
import json
from packets.packet import Packet

class SettingPacket(Packet):
    def type_str(self) -> str:
        return "setting"

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
        if not (10 < (255 - b[21]) / 8 < 28):
            return False
        if not (10 < (255 - b[22]) / 8 < 28):
            return False
        return True

    @property
    def low_temp(self) -> float:
        return (255 - self._bytes[21]) / 8

    @property
    def hi_temp(self) -> int:
        return (255 - self._bytes[22]) / 8

    @property
    def hops(self) -> str:
        match self._bytes[19]:
            case 0: return "Direct"
            case 1: return "Transit"
            case 2: return "Final"
            case _: return "<unknown>"

    @property
    def mode(self) -> int:
        return self._bytes[20]

    @property
    def mode_string(self) -> str:
        match self.mode:
            case 0: return "Eco"
            case 1: return "Comfort"
            case 2: return "Away"
            case 3: return "Off"
            case _: return "<unknown>"

    @staticmethod
    def known_fields() -> list[int]:
        return [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 21, 22]

    def to_json(self) -> str:
        return json.dumps(
            {"type": self.type_str(),
            "low_temp": self.low_temp,
            "hi_temp": self.hi_temp})

    def __str__(self) -> str:
        return (f"{self.receiver:>8}: Setting: {self.addr1:>8}, "
                f"{str(self.addr2):>8}, {str(self.addr3):>8}: "
                f"{self.low_temp}°C, {self.hi_temp}°C, "
                f"{self.mode_string}, {self.hops}, {self.unknown()}")
