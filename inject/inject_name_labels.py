import io
from pathlib import Path
from tqdm import tqdm
from classes.pointers import Pointer, PointerList
from config import defaults
from utils import helpers

EXIT_BYTE = b'\x00'
PADDING = EXIT_BYTE * 4
SPACING = 64

def inject_name_labels(input_rompath=None, output_rompath=defaults.OUTPUT_ROM, files=Path("inject/name_labels")):
    """Overwrite name with pointer, then write new data at the pointer location"""
    print("Inserting Name Labels")
    rom = helpers.ensure_output_rompath(input_rompath, output_rompath)
    files = helpers.get_files(files, ".txt")
    files = sorted(files, key=lambda f: int(Path(f).stem, 16))
    with open(rom, "r+b") as f:
        pointer_saki = helpers.find_juicy_insert_position(size=32, start=defaults.BLANKSPACE_STARTPOS, rompath=output_rompath)
        for i, file in enumerate(tqdm(files)):
            with open(file, "rb") as fp:
                data = fp.read()
            start = int(file.stem, 16)
            pointer_saki += SPACING
            pointer = Pointer.from_be_int(pointer_saki + 0x8000000)
            f.seek(start)
            f.write(pointer)
            f.seek(pointer_saki)
            data += PADDING
            #print(f"Data: {data.hex(' ')}, Pointer: {hex(int(pointer))}, Insert_POS: {hex(pointer_saki)}")
            f.write(data)


