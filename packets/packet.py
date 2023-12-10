from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from utils import toaddr, known_addresses, crc16

class CRCError(Exception):
    pass

class ParseError(Exception):
    pass

@dataclass
class Packet(ABC):
    _address: str
    _bytes: bytearray

    @classmethod
    def from_hex(cls, data: str) -> Packet:
        if len(data[8:-4]) != 64:
            # Sometimes there's an extra character at the end of the line.
            data = data[:-1]
        address = data[0:8]
        payload = data[8:-4]
        crc = data[-4:]

        try:
            full_msg = bytearray.fromhex(data[:-4])
        except ValueError:
            raise ParseError(f"Could not parse '{data[:-4]}'")

        calculated_crc = crc16(full_msg, 0, len(full_msg))
        calculated_crc = f"{calculated_crc:#0{6}x}"[2:]
        if crc != calculated_crc:
            raise CRCError(f"Calculated CRC '{calculated_crc}' does not match '{crc}'")

        from packets.setting_packet import SettingPacket
        from packets.status_packet import StatusPacket

        if StatusPacket.can_parse(bytearray.fromhex(payload)):
            return StatusPacket(address, bytearray.fromhex(payload))
        if SettingPacket.can_parse(bytearray.fromhex(payload)):
            return SettingPacket(address, bytearray.fromhex(payload))

        return UnknownPacket(address, bytearray.fromhex(payload))

    @property
    def receiver(self) -> str | None:
        return known_addresses.get(self._address, None)

    @staticmethod
    @abstractmethod
    def can_parse(b: bytearray) -> bool:
        """Whether this can be parsed."""

    @property
    def addr1(self) -> str | None:
        addr = toaddr(self._bytes, 3, 4, 5, 6)
        return known_addresses[addr] if addr else None

    @property
    def addr2(self) -> str | None:
        addr = toaddr(self._bytes, 7, 8, 9, 10)
        return known_addresses[addr] if addr else None

    @property
    def addr3(self) -> str | None:
        addr = toaddr(self._bytes, 11, 12, 13, 14)
        return known_addresses[addr] if addr else None

    def from_addr(self) -> str:
        return self.addr3 if self.addr3 else self.addr2

    @abstractmethod
    def to_json(self) -> str:
        """Convert to JSON."""

    @staticmethod
    def known_fields() -> list[int]:
        return []

    @abstractmethod
    def type_str(self) -> str:
        """Type of packet."""

    def unknown(self) -> list[int]:
        return [
            self._bytes[i]
            for i in range(0, len(self._bytes))
            if i not in self.known_fields()
        ]


class UnknownPacket(Packet):
    @staticmethod
    def can_parse(b: bytearray) -> bool:
        return True

    def _is_addr(self, i: int) -> str | None:
        if i + 3 >= len(self._bytes):
            return None
        addr = toaddr(self._bytes, i, i + 1, i + 2, i + 3)
        if addr is None or addr not in known_addresses:
            return None
        return known_addresses[addr]

    def to_json(self) -> str:
        return "{}"

    def type_str(self) -> str:
        return "unknown"

    def __str__(self) -> str:
        s = f"{self.receiver}: Unknown: "
        i = 0
        zeros = 0
        while i < len(self._bytes):
            addr = self._is_addr(i)
            if addr is not None:
                s += f" [{addr}] "
                i += 4
            elif self._bytes[i] == 0:
                zeros += 1
                i += 1
            else:
                if zeros > 0:
                    s += f" ({zeros} zeros) "
                    zeros = 0
                s += f"{self._bytes[i]:02x}({int(self._bytes[i])}) "
                i += 1
        if zeros > 0:
            s += f" ({zeros} zeros) "
            zeros = 0
        return s
