import io
from pathlib import Path
from tqdm import tqdm
from classes.pointers import Pointer, PointerList, inject_ptrlist
from config import defaults
from utils import helpers

# lol, you will need an ASM hack to make the menu bigger
# also you are repeating yourself a lot in inject_name_labels
BREAK_BYTE = b"\x00\x00"
NEW_BASE_ADDR = Pointer.from_be_int(0x0877a220)

def inject_menu(input_rompath=None, output_rompath=defaults.OUTPUT_ROM, files=Path("inject/menu")):
    """check if name bytes can be injected without disruptig offset,
       then inject."""
    print("Inserting Menu Items")
    rom = helpers.ensure_output_rompath(input_rompath, output_rompath)

    ptrs = PointerList(start_addr=0x8ba10, end_addr=0x8ba17, rompath=rom)
    ptrs2 = PointerList(start_addr=0x8ba6c, end_addr=0x8ba73, rompath=rom)
    ptrs3 = PointerList(start_addr=0x8ba78, end_addr=0x8ba7b, rompath=rom)
    ptrs4 = PointerList(start_addr=0x8baac, end_addr=0x8baaf, rompath=rom)
    full_ptrlist = [ptrs, ptrs2, ptrs3, ptrs4]

    inject_ptrlist(ptrs)

    files = helpers.get_files(files, ".txt")
    files = sorted(files, key=lambda f: int(Path(f).stem, 16))
    offset = 0

    with open(rom, "r+b") as f:
        for file in tqdm(files):
            start = int(NEW_BASE_ADDR) - 0x08000000 + offset
            newptr = Pointer.from_be_int(int(NEW_BASE_ADDR) + offset)
            oldptr = Pointer.from_be_int(int(file.stem, 16) + + 0x08000000)

            for sub_ptrlist in full_ptrlist:
                sub_ptrlist.replace(oldptr, newptr)

            with open(file, "rb") as f2:
                data = f2.read()
                data += BREAK_BYTE
                f.seek(start)
                offset += len(data)
                f.write(data)

    for sub_ptrlist in full_ptrlist:
        inject_ptrlist(sub_ptrlist)
