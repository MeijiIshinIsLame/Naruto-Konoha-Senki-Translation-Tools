import io
from dataclasses import dataclass, field
from pathlib import Path

class Pointer(bytes):
    """Represents a pointer as raw little-endian bytes"""
    def __int__(self):
        # interpret the bytes as a little-endian integer
        return int.from_bytes(self, "little")
    
    @classmethod
    def from_be_bytes(cls, data: bytes):
        """Create a Pointer from big-endian bytes by reversing the byte order."""
        return cls(data[::-1])
        
    @classmethod
    def from_be_int(cls, data: int):
        """Create a Pointer from big-endian int and convert to little endian"""
        return cls(data.to_bytes(4, "little"))
        
@dataclass
class PointerList:
    """Represents a collection of pointers within a binary ROM."""
    start_addr: int
    end_addr: int
    rompath: Path
    #ensures new list instance
    ptrs: list[Pointer] = field(default_factory=list)

    def __post_init__(self):
        """Populate pointers immediately after initialization."""
        self.populate(rompath=self.rompath)

    def __len__(self):
        return len(self.ptrs)

    def __getitem__(self, index):
        return self.ptrs[index]

    def __setitem__(self, index, value):
        self.ptrs[index] = value
    
    def __iter__(self):
        return iter(self.ptrs)
        
    def populate(self, rompath: Path):
        """Populate offsets in range from a file handle"""
        with open(rompath, "rb") as f:
            f.seek(self.start_addr)
            while f.tell() <= self.end_addr:
                data = f.read(4)
                if len(data) < 4:
                    break
                self.ptrs.append(Pointer(data))
    
    def replace(self, old, new):
        """replace an item in the list for all occurences"""
        for i, ptr in enumerate(self.ptrs):
            if ptr == old:
                self.ptrs[i] = new

def inject_ptrlist(ptrlist):
    """Write pointers from pointerlist into ROM as bytes"""
    with open(ptrlist.rompath, "r+b") as f:
        f.seek(ptrlist.start_addr)
        for ptr in ptrlist:
            f.write(ptr)
