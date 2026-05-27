from pathlib import Path

konohasenki = Path(r"../../game/Naruto - Konoha Senki English translation.gba")

class CPU:
    def __init__(self):
        self.r0  = 0x00000000
        self.r1  = 0x00008c89
        self.r2  = 0x00000020
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

cpu.lsr("r4", "r1", 0x8)
print("lsr r4, r1, 0x8")
cpu.pprint("r4")

cpu._and("r1", "r1", 0xff)
print("lsl r1, 0xff")
cpu.pprint("r1")

"""
i = 0
while i <= 32:
    with open(logf, 'a') as f:
        print("##############################")
        print(f"RUN {i}")
        print("##############################")
        print("original")
        f.write("##############################\n")
        f.write(f"RUN {i}\n")
        f.write("##############################\n")
        f.write("original\n")
    cpu.pprint()

""""""
    cpu.ldrb("r2", "r5")
    print("ldrb r2, r5")
    cpu.pprint("r2")

    cpu.mov("r1", 0x3)
    print("mov r1, 0x3")
    cpu.pprint("r1")

    cpu._and("r1", "r2")
    print("ands r1, r2")
    cpu.pprint("r1")

    cpu.mov("r7", "r10")
    print("mov r7, r10")
    cpu.pprint("r7")

    cpu.orr("r1", "r7")
    print("orrs r1, r7")
    cpu.pprint("r1")

    cpu.mov("r0", 0xc)
    print("mov r0, 0xC")
    cpu.pprint("r0")

    cpu._and("r0", "r2")
    print("ands r0, r2")
    cpu.pprint("r0")

    cpu.mov("r7", "r9")
    print("mov r7, r9")
    cpu.pprint("r7")

    cpu.orr("r0", "r7")
    print("orrs r0, r7")
    cpu.pprint("r0")

    cpu.lsl("r0", "r0", 0x2)
    print("lsl r0, r0, #0x2")
    cpu.pprint("r0")

    cpu.orr("r1", "r0")
    print("orrs r1, r0")
    cpu.pprint("r1")

    cpu.mov("r0", 0x30)
    print("mov r0, #0x30")
    cpu.pprint("r0")

    cpu._and("r0", "r2")
    print("ands r0, r2")
    cpu.pprint("r0")

    cpu.mov("r7", "r8")
    print("mov r7, r8")
    cpu.pprint("r7")

    cpu.orr("r0", "r7")
    print("orrs r0, r7")
    cpu.pprint("r0")

    cpu.lsl("r0", "r0", 0x4)
    print("lsl r0, r0, #0x4")
    cpu.pprint("r0")

    cpu.orr("r1", "r0")
    print("orrs r1, r0")
    cpu.pprint("r1")

    cpu.mov("r0", 0xC0)
    print("mov r0, #0xC0")
    cpu.pprint("r0")

    cpu._and("r0", "r2")
    print("ands r0, r2")
    cpu.pprint("r0")

    cpu.mov("r2", "r12")
    print("mov r2, r12")
    cpu.pprint("r2")

    cpu.orr("r0", "r2")
    print("orrs r0, r2")
    cpu.pprint("r0")

    cpu.lsl("r0", "r0", 0x6)
    print("lsl r0, r0, #0x6")
    cpu.pprint("r0")

    cpu.orr("r1", "r0")
    print("orrs r1, r0")
    cpu.pprint("r1")

    cpu._add("r3", "r3", 0x2)
    print("add r3, #0x2")
    cpu.pprint("r3")

    cpu._add("r5", "r5", 0x1)
    print("add r5, #0x1")
    cpu.pprint("r5")

    cpu._add("r0", "r6", 0x1)
    print("add r0, r6, #0x1")
    cpu.pprint("r0")

    cpu.lsl("r0", "r0", 0x18)
    print("lsl r0, r0, #0x18")
    cpu.pprint("r0")

    cpu.lsr("r6", "r0", 0x18)
    print("lsr r6, r0, #0x18")
    cpu.pprint("r6")

    i += 1
"""