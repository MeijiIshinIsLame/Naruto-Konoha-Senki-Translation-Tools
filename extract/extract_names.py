import io
from pathlib import Path
from classes.pointers import Pointer, PointerList

START = 0x599280
END = 0x599924 #possibly 24 check after
EXIT_BYTE = b'\x00'

def read_until(f, exit_byte=EXIT_BYTE):
    b = f.read(1)
    while b != exit_byte:
        b += f.read(1)
    return b

def extract(input_rompath):
    ptrs = PointerList(start_addr=START, end_addr=END, rompath=input_rompath)
    print(ptrs)
    with open(input_rompath, "rb"):   
        for ptr in ptrs:
            b = read_until(EXIT_BYTE)
           
        