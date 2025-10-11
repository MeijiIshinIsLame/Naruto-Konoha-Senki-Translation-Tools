import io
import os
import re
import codecs
import shutil
from pathlib import Path
from tqdm import tqdm
from utils import helpers
from classes.pointers import Pointer, PointerList
from config import defaults

class Script:
    def __init__(self, path):
        self.path = Path(path)
        self.contents = self.parse_script()
        self.base_addr = int(self.path.stem, 16)
    
    def __len__(self):
        return sum(len(i) for i in self.contents)
    
    def parse_script(self):
        """turn script TXT file into a list of btyes() objects"""
        tag_re = re.compile(r"<(HEX|ADDR|SJIS)>(.*?)</\1>", re.DOTALL)
        data = ""
        out = []
        with open(self.path, "r", encoding="shift_jis") as f:
            data = f.read()
        for tag, body in tag_re.findall(data):
            body = body.strip()
            if tag == "HEX":
                out.append((tag, bytes.fromhex(body)))
            elif tag == "ADDR":
                out.append((tag, bytes.fromhex(body)))
            elif tag == "SJIS":
                out.append((tag, body.encode("shift_jis")))
            else:
                out.append((tag, body))
        return out
        
def inject_ptrlist(ptrlist):
    """Write pointers from pointerlist into ROM as bytes"""
    with open(ptrlist.rompath, "r+b") as f:
        f.seek(ptrlist.start_addr)
        for ptr in ptrlist:
            f.write(ptr)

def inject_script(pos, script, f, output_rompath=defaults.OUTPUT_ROM):
    """inject the bytes of a script to a position in a file"""
    b = bytes()
    ptrs = PointerList(start_addr=0x60C78, end_addr=0x60FAB, rompath=output_rompath)
    script_base_addr = Pointer.from_be_int(script.base_addr)
    new_base_addr = Pointer.from_be_int(pos + 0x8000000)
    ptrs.replace(old=script_base_addr, new=new_base_addr)
    inject_ptrlist(ptrs) #we may not have to do this over and over lol
    
    for item in script.contents:
        if item[0] == "ADDR":
            ptr = Pointer(item[1])
            offset = int(ptr) - script.base_addr
            updated_ptr = Pointer.from_be_int(pos + offset + 0x8000000)
            b += updated_ptr
        else:
            b += item[1]
    f.seek(pos)
    f.write(b)

def inject_dialog_scripts(input_rompath=None, scripts_path=defaults.INJECT_SCRIPTS_PATH, output_rompath=defaults.OUTPUT_ROM):
    """inject all the dialog scripts into ROM"""
    files = helpers.get_files(path=scripts_path)
    helpers.ensure_output_rompath(input_rompath, output_rompath)
    ptrs = PointerList(start_addr=0x60C78, end_addr=0x60FAB, rompath=output_rompath)
    print("Inserting Dialog")
    pos = 0x5AE750 #initial pos to start searching for insert space
    for file in tqdm(files):
        script = Script(file)
        insert_pos = helpers.find_juicy_insert_position(
            size=len(script),
            start=pos,
            rompath=output_rompath
        )
        with open(output_rompath, "r+b") as f:
            inject_script(insert_pos, script, f, output_rompath)
            pos = f.tell()