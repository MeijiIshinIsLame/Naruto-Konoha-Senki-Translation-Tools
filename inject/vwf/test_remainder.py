start = 0x060021f0
end = 0x06002160

ramlen = start - end + 16

RED = "\033[31m"
RESET = "\033[0m"


class CPU:
    def __init__(self, ramlen):
        self.start = 0x060021a0
        self.end = 0x06002160
        self.ramlen = ramlen
        self.ram = ram = "00" * ramlen
        self.addr_pointer = 0x060021a0

    def print_ram(self, highlightpos=None):
        if highlightpos is None:
            highlightpos = self.addr_pointer

        for offset in range(0, self.ramlen, 16):
            b = ""

            for byte in range(offset, offset + 16):
                byte_addr = self.end + byte
                value = self.ram[byte * 2:byte * 2 + 2]

                if highlightpos <= byte_addr < highlightpos + 2:
                    b += f"{RED}{value}{RESET} "
                else:
                    b += f"{value} "

            addr = self.end + offset
            print(f"{addr:#010x}: {b}")

        print("\n\n")

    def draw_image(self):
        pass
        
    def go_forwards(self, num, printing=False):
        before = self.addr_pointer
        self.addr_pointer += num
        if printing:
            print(f"adding {hex(num)} to {hex(before)}: {hex(self.addr_pointer)}")
            self.print_ram(self.addr_pointer)
    
    def go_back(self, num, printing=False):
        before = self.addr_pointer
        self.addr_pointer -= num
        if printing:
            print(f"subbing {hex(num)} to {hex(before)}: {hex(self.addr_pointer)}")
            self.print_ram(self.addr_pointer)

    def get_2bytes(self):
        offset = self.addr_pointer - self.end
        pos = offset * 2
        b = self.ram[pos:pos+4]
        left = b[0:2]
        right = b[2:4]
        result = right + left
        print(f"got {result} from pos {hex(self.addr_pointer)}")
        self.print_ram(self.addr_pointer)
        return result
    
    def insert_2bytes(self, value):
        offset = self.addr_pointer - self.end
        pos = offset * 2
        left = value[0:2]
        right = value[2:4]
        newval = right + left
        result = self.ram[:pos] + newval + self.ram[pos + len(newval):]
        self.ram = result
        print(f"inserted {value} to pos {hex(self.addr_pointer)}")
        self.print_ram(self.addr_pointer)



############ LEN 7 #############
cpu = CPU(ramlen)

cpu.go_back(0x3e)
cpu.insert_2bytes("8000")

cpu.go_forwards(0x3e)
cpu.insert_2bytes("0888")

cpu.go_forwards(0x0)
cpu.insert_2bytes("8000")

cpu.go_forwards(0x2)
cpu.insert_2bytes("0888")

###################this is where shit gets fucked

for i in range(0, 15):
    cpu.go_back(0x3c)
    cpu.insert_2bytes("8000")

    cpu.go_forwards(0x3e)
    cpu.insert_2bytes("0888")

    cpu.go_forwards(0x0)
    cpu.insert_2bytes("8000")

    cpu.go_forwards(0x2)
    cpu.insert_2bytes("0888")


#cpu.insert_2bytes("1234")
#print(cpu.get_2bytes())

