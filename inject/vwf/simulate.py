from pathlib import Path

konohasenki = Path(r"../../game/Naruto - Konoha Senki English translation.gba")

class CPU:
    def __init__(self):
        self.r0  = 0x00009ba5
        self.r1  = 0x00008c89
        self.r2  = 0x00000004
        self.r3  = 0x060021A0
        self.r4  = 0x03001170
        self.r5  = 0x080A2154
        self.r6  = 0x00000000
        self.r7  = 0x00000080
        self.r8  = 0x00000080
        self.r9  = 0x00000020
        self.r10 = 0x00000008
        self.r11 = 0x00000000
        self.r12 = 0x00000200
        self.r13 = 0x03001170
        self.logf = Path("log.txt")

    def ldrb(self, dest, src):
        addr = getattr(self, src)
        with open(konohasenki, "rb") as f:
            f.seek(addr - 0x08000000)
            val = f.read(1)
        val = val[0] & 0xFFFFFFFF

        setattr(self, dest, val)
        self.writelog_custom(f"ldrb {dest}, {src}\n")

    def _add(self, dest, src, val=None):
        if not val:
            val = getattr(self, src)
            newval = (getattr(self, dest) + val) & 0xFFFFFFFF
        else:
            newval = (getattr(self, src) + val) & 0xFFFFFFFF
        setattr(self, dest, newval)
        self.writelog_custom(f"add {dest}, {src}, {val}\n")

    def orr(self, dest, src, val=None):
        if not val:
            val = getattr(self, src)
            newval = (getattr(self, dest) | val) & 0xFFFFFFFF
        else:
            newval = (getattr(self, src) | val) & 0xFFFFFFFF
        setattr(self, dest, newval)
        self.writelog_custom(f"orr {dest}, {src}, {val}\n")
    
    def _and(self, dest, src, val=None):
        if not val:
            val = getattr(self, src)
            newval = (getattr(self, dest) & val) & 0xFFFFFFFF
        else:
            newval = (getattr(self, src) & val) & 0xFFFFFFFF
        setattr(self, dest, newval)
        self.writelog_custom(f"and {dest}, {src}, {val}\n")
    
    def lsl(self, dest, src, val=None):
        if not val:
            val = getattr(self, src)
            newval = (getattr(self, dest) << val) & 0xFFFFFFFF
        else:
            newval = (getattr(self, src) << val) & 0xFFFFFFFF
        setattr(self, dest, newval)
        self.writelog_custom(f"lsls {dest}, {src}, {val}\n")

    def lsr(self, dest, src, val=None):
        if not val:
            val = getattr(self, src)
            newval = (getattr(self, dest) >> val) & 0xFFFFFFFF
        else:
            newval = (getattr(self, src) >> val) & 0xFFFFFFFF
        setattr(self, dest, newval)
        self.writelog_custom(f"llsrs {dest}, {src}, {val}\n")

    def mov(self, dest, src):
        if type(src) == str:
            src = getattr(self, src)
        setattr(self, dest, src)
        self.writelog_custom(f"mov {dest}, {src}\n")

    def mul(self, dest, src, val=None):
        if val is None:
            val = getattr(self, src)
            newval = (getattr(self, dest) * val) & 0xFFFFFFFF
        else:
            newval = (getattr(self, src) * val) & 0xFFFFFFFF

        setattr(self, dest, newval)
        self.writelog_custom(f"mul {dest}, {src}, {val}\n")

    def sub(self, dest, src, val=None):
        if val is None:
            val = getattr(self, src)
            newval = (getattr(self, dest) - val) & 0xFFFFFFFF
        else:
            newval = (getattr(self, src) - val) & 0xFFFFFFFF
        setattr(self, dest, newval)
        self.writelog_custom(f"sub {dest}, {src}, {val}\n")

    def pprint(self, emphasis=None):
        RED = "\033[31m"
        WHITE = "\033[37m"
        regs = {
            "r0":  self.r0,
            "r1":  self.r1,
            "r2":  self.r2,
            "r3":  self.r3,
            "r4":  self.r4,
            "r5":  self.r5,
            "r6":  self.r6,
            "r7":  self.r7,
            "r8":  self.r8,
            "r9":  self.r9,
            "r10": self.r10,
            "r11": self.r11,
            "r12": self.r12,
            "r13": self.r13,
        }
        for k, v in regs.items():
            SPACES = "  "
            if len(k) > 2:
                SPACES = " "
            if k == emphasis:
                print(f"{RED}{k}:{SPACES}{v:08X}{RED}")
            else:
                print(f"{WHITE}{k}:{SPACES}{v:08X}{WHITE}")
        print("-------------------------------------------------")
        self.writelog()

    def writelog(self):

        regs = {
            "r0":  self.r0,
            "r1":  self.r1,
            "r2":  self.r2,
            "r3":  self.r3,
            "r4":  self.r4,
            "r5":  self.r5,
            "r6":  self.r6,
            "r7":  self.r7,
            "r8":  self.r8,
            "r9":  self.r9,
            "r10": self.r10,
            "r11": self.r11,
            "r12": self.r12,
            "r13": self.r13,
        }
        for k, v in regs.items():
            SPACES = "  "
            if len(k) > 2:
                SPACES = " "
            with open(self.logf, "a") as f:
                f.write(f"{k}:{SPACES}{v:08X}\n")
        with open(self.logf, "a") as f:
            f.write("-------------------------------------------------\n")

    def writelog_custom(self, data):
        with open(self.logf, 'a') as f:
            f.write(data)

cpu = CPU()

logf = Path("log.txt")
with open(logf, 'w') as f:
    pass

######################## setup ls for vram ########################
cpu.mov("r4", 0x4)
print("mov r4, 0x4")
cpu.pprint("r4")

cpu.mov("r5", 0x10)
print("mov r5, 0x16")
cpu.pprint("r5")

cpu.mov("r6", 0x4)
print("mov r6, 0x4")
cpu.pprint("r6")

cpu.mul("r6", "r2")
print("mul r6, r2")
cpu.pprint("r6")

cpu._add("r5", "r6")
print("add r5, r6")
cpu.pprint("r5")

cpu.lsl("r0", "r5")
print("lsl r0, r5")
cpu.pprint("r0")

cpu.lsr("r0", "r5")
print("lsr r0, r5")
cpu.pprint("r0")

######################## setup ls for chars ########################

#cpu.mov("r4", 0x4)
#print("mov r4, 0x4")
#cpu.pprint("r4")

cpu.mov("r5", 0x4)
print("mov r5, 0x4")
cpu.pprint("r5")

cpu.sub("r5", "r2")
print("sub r5, r2")
cpu.pprint("r5")

cpu.mul("r5", "r5", 0x4)
print("add r5, 0x4")
cpu.pprint("r5")

cpu.lsr("r1", "r5")
print("lsr r0, r5")
cpu.pprint("r1")

cpu.lsl("r1", "r5")
print("lsl r0, r5")
cpu.pprint("r1")

######################## build the final and bx ########################

cpu.orr("r1", "r0")
print("orr r1, r0")
cpu.pprint("r1")

"""
;r0 = halfword pulled from vram
;r1 = halfword pulled from rom
;r2 = pos to start inserting 1-4 (from left to right as pixels - 12 34)
;
;at the end, r1 is the final thing 
;
create_4pixel_block:
    mov r4, 4h ; shift amount
    mov r5, 16h ;hard shift for the vram pull
    mov r6, 4h ; minus for remainder

    mul r4, r2
    add r5, r4
    
    lsl r0, r5
    lsr r0, r5
    lsr r1, r4
    lsl r1, r4
    
    and r0, r1
    sub r2, r4 
    bx lr
"""