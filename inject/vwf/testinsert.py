bchar = bytes.fromhex("8888888888888888BBBB89889B999B889B889B889B889B889B889B88BBBB8988")
cchar = bytes.fromhex("9B999B889B889B889B889B889B889B88BBBB8988999988888888888888888888")
zeros = bytes.fromhex("00") * len(bchar)
rambytes = bchar + zeros
class RAM:
    def __init__(self, rambytes):
        self.rambytes = rambytes
    
    def ldrh(self, pos):
        lo = self.rambytes[pos]
        hi = self.rambytes[pos + 1]
        return lo | (hi << 8)
    
    def ldrb():
        pass

ram = RAM(rambytes)
cchar_ram = RAM(cchar)
print(hex(ram.ldrh(31)))
print(ram.rambytes)