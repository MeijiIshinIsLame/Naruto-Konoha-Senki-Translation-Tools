import io
from pathlib import Path
from tqdm import tqdm
from utils import helpers
from config import defaults
from classes.pointers import Pointer, PointerList

START = 0x599280
END = 0x599920
EXIT_BYTE = b'\x00'

class Entity:
    def __init__(self, path):
        self.path = Path(path)
        self.contents = self.parse_entity()
        self.base_addr = int(self.path.stem, 16)
    
    def __len__(self):
        return len(self.contents)
    
    def parse_entity(self):
        """turn entity TXT file into a list of btyes() objects"""
        with open(self.path, "r", encoding="shift_jis") as f:
            data = f.read().strip("\n").encode('shift_jis') + EXIT_BYTE
        return data

def inject_ptrlist(ptrlist):
    """Write pointers from pointerlist into ROM as bytes"""
    with open(ptrlist.rompath, "r+b") as f:
        f.seek(ptrlist.start_addr)
        for ptr in ptrlist:
            f.write(ptr)
            
def inject_entity(pos, entity, f, output_rompath=defaults.OUTPUT_ROM):
    """inject the bytes of a entity to a position in a file"""
    ptrs = PointerList(start_addr=START, end_addr=END, rompath=output_rompath)
    entity_base_addr = Pointer.from_be_int(entity.base_addr)
    new_base_addr = Pointer.from_be_int(pos + 0x8000000)
    ptrs.replace(old=entity_base_addr, new=new_base_addr)
    inject_ptrlist(ptrs) #we may not have to do this over and over lol
    f.seek(pos)
    f.write(entity.contents)
    
def inject_entities(input_rompath=None, entities_path=defaults.INJECT_ENTITIES_PATH, output_rompath=defaults.OUTPUT_ROM):
    """inject all the entities into ROM"""
    files = helpers.get_files(path=entities_path)
    helpers.ensure_output_rompath(input_rompath, output_rompath)
    print("Inserting Entities")
    pos = 0x5AE750 #initial pos to start searching for insert space
    for file in tqdm(files):
        entity = Entity(file)
        insert_pos = helpers.find_juicy_insert_position(
            size=len(entity),
            start=pos,
            rompath=output_rompath
        )
        with open(output_rompath, "r+b") as f:
            #print(f"Inserting at {hex(insert_pos)} entity with contents {entity.contents}")
            inject_entity(insert_pos, entity, f, output_rompath)
            pos = f.tell()