from pathlib import Path
from utils import helpers
from classes.pointers import Pointer, PointerList
from config import defaults
from typing import BinaryIO

ADDRESS = 0
HEX = 1
SJIS_TEXT = 2
END_DIALOG = b'\x00\x00' #opcode that means end of dialog
SJIS_DICT = helpers.create_tbl_dict(Path(defaults.SJIS_TBL))
LINEBREAK_OPCODE = 0x0a

def decode_sjis(b: bytes, tbl: dict[str, str]):
    ONE_BYTE = 2
    TWO_BYTES = 4
    bstring = str(b.hex()).upper()
    i = 0
    out_string = ""

    while True:
        if i > len(bstring):
            break

        #check for 2byte pattern
        byte = bstring[i:i+TWO_BYTES]
        if byte in tbl:
            out_string += tbl[byte]
            i += TWO_BYTES
            continue

        #check for 1byte pattern
        byte = bstring[i:i+ONE_BYTE]
        if byte in tbl:
            out_string += tbl[byte]
            i += ONE_BYTE
            continue

        #if nothing just incriment ig
        i += ONE_BYTE
    print(out_string)
    return out_string

def is_address(b: bytes):
    ptr = int.from_bytes(b, "little")
    return 0x08000000 <= ptr <= 0x087ffff0

def read_ahead(f: BinaryIO, howfar: int):
    b = f.read(howfar)
    f.seek(f.tell() - howfar)
    return b

class DialogBuffer:
    def __init__(self, f: BinaryIO, pointer: Pointer):
        self.f = f
        self.pointer = pointer

    def read_until(self, stopcode: bytes):
        b = b''
        start = int(self.pointer) - 0x08000000
        print("START", self.pointer)
        self.f.seek(start)
        stopcode_check = read_ahead(self.f, len(stopcode))
        while True:
            if not stopcode_check:
                break
            if stopcode_check == stopcode:
                b += stopcode
                break
            b += self.f.read(1)
            stopcode_check = read_ahead(self.f, len(stopcode))
        return b

class Dialog:
    def __init__(self, data: bytes):
        self.data = data
        self.parsed_data = ""
        self.currentpos = 0

    def parse_data(self):
        while self.currentpos < len(self.data):
            print(f"currentpos: {hex(self.currentpos)}, len {hex(len(self.data))}")
            opcode = self.data[self.currentpos]
            epicly_parsed_data = process_opcode(opcode, self)
            self.parsed_data += epicly_parsed_data
        return self.parsed_data #i know we dont have to but just for readability

    def read(self, numbytes: int):
        data = self.data[self.currentpos: self.currentpos + numbytes]
        self.currentpos += numbytes
        return DialogBytes(data)

    def read_the_rest(self):
        #we convert to bytes because if its only one byte it will be processed as an int lol
        #i dont make the rulez
        data = bytes(self.data[self.currentpos:])
        self.currentpos = len(data)
        return DialogBytes(data)

    def read_until_address(self):
        data_to_process = b''
        addr_check = self.data[self.currentpos: self.currentpos + 4]
        while not is_address(addr_check):
            if self.currentpos >= len(self.data):
                break
            data_to_process += self.read(1).data
            addr_check = self.data[self.currentpos: self.currentpos + 4]
        return DialogBytes(data_to_process)

    def read_until_opcode(self):
        data_to_process = b''
        while True:
            read_2_ahead = self.data[self.currentpos: self.currentpos + 2]
            if self.currentpos >= len(self.data):
                break
            if helpers.is_2byte_sjis(read_2_ahead):
                data_to_process += self.read(2).data
            elif helpers.is_1byte_sjis(bytes(read_2_ahead[0])):
                data_to_process += self.read(1).data
            else:
                break
            #print("read 2 ahead", read_2_ahead.hex())
        #print("fuckin SJIS data: ", data_to_process)
        return DialogBytes(data_to_process)

    def read_until_sjis(self):
        data_to_process = b''
        while True:
            read_2_ahead = self.data[self.currentpos: self.currentpos + 2]
            if self.currentpos >= len(self.data):
                break
            if helpers.is_sjis(read_2_ahead):
                break
            data_to_process += self.read(1).data
        #print("Non-SJIS data: ", data_to_process)
        return DialogBytes(data_to_process)

    def oops_all_sjis_and_hex(self):
        processed_data = ""
        while self.currentpos < len(self.data):
            processed_data += self.read_until_sjis().process_as(HEX)
            a = self.read_until_opcode()
            processed_data += a.process_as(SJIS_TEXT)
        return processed_data

class DialogBytes:
    def __init__(self, data: bytes):
        self.data = data

    def process_as(self, how: int):
        if how == ADDRESS:
            return f"<ADDR>{self.data.hex()}</ADDR>\n"
        if how == HEX:
            return f"<HEX>{self.data.hex()}</HEX>\n"
        if how == SJIS_TEXT:
            #print(self.data)
            sjis_text = decode_sjis(self.data, SJIS_DICT)
            return f"<SJIS>{sjis_text}</SJIS>\n<TRANSLATION>{sjis_text}</TRANSLATION>\n"
        return None

def process_opcode(opcode: int, dialog: Dialog):
    if dialog.currentpos > len(dialog.data):
        return None

    if opcode == 0x01:

        part1 = dialog.read(1).process_as(HEX)
        part2 = dialog.read_the_rest().process_as(SJIS_TEXT)
        return part1 + part2

    if opcode == 0x12:
        header = dialog.read_until_sjis().process_as(HEX)
        return header + dialog.oops_all_sjis_and_hex()

    if opcode == 0x15:
        part1 = dialog.read(4).process_as(HEX)
        part2 = dialog.read(4).process_as(ADDRESS)
        return part1 + part2

    if opcode == 0x16:
        return dialog.read_the_rest().process_as(HEX)

    if opcode == 0x22:
        part1 = dialog.read(16).process_as(HEX)
        part2 = dialog.oops_all_sjis_and_hex()
        return part1 + part2

    if opcode == 0x32:
        part1 = dialog.read(1).process_as(HEX)
        part2 = dialog.read(4).process_as(ADDRESS)
        return part1 + part2

    if opcode == 0x33:
        part1 = dialog.read_until_address().process_as(HEX)
        part2 = dialog.read(4).process_as(ADDRESS)
        return part1 + part2

    if opcode == 0x34:
        part1 = dialog.read(4).process_as(HEX)
        part2 = dialog.read(4).process_as(ADDRESS)
        return part1 + part2

    if opcode == 0x1B:
        header = dialog.read_until_sjis().process_as(HEX)
        return header + dialog.oops_all_sjis_and_hex()

    if opcode == 0x0B:
        part1 = dialog.read(2).process_as(HEX)
        part2 = dialog.read(4).process_as(ADDRESS)
        return part1 + part2

    if opcode == 0x08:
        part1 = dialog.read_until_sjis().process_as(HEX)
        part2 = dialog.oops_all_sjis_and_hex()
        return part1 + part2

    if opcode == 0x1E:
        return dialog.read_the_rest().process_as(HEX)

    if opcode == 0x0C:
        part1 = dialog.read(2).process_as(HEX)
        part2 = dialog.read(4).process_as(ADDRESS)
        part3 = dialog.oops_all_sjis_and_hex()
        return part1 + part2 + part3

    if opcode == 0x07:
        part1 = dialog.read(1).process_as(HEX)
        part2 = dialog.read(4).process_as(ADDRESS)
        part3 = dialog.read(1).process_as(HEX)
        return part1 + part2 + part3

    # opcodes not handled yet
    return dialog.oops_all_sjis_and_hex()

def extract_dialogs(rom, out_path=Path("./extract/script_files")):
    ptrs = PointerList(start_addr=0x60C78, end_addr=0x60FAB, rompath=rom)
    for ptr in ptrs:
        data = b''
        if int(ptr) > 0x08000000:
            filename = f"{str(ptr)}.txt"
            filepath = out_path / filename
            with open(rom, "rb") as f:
                dialog_buffer = DialogBuffer(f, ptr)
                data = dialog_buffer.read_until(END_DIALOG)
            processed_data = Dialog(data).parse_data()
            with open(filepath, "w") as f:
                f.write(processed_data)
        else:
            continue
    print(ptrs)
