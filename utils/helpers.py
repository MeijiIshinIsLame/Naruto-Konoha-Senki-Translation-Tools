import io
import shutil
from pathlib import Path
from config import defaults

SJIS_FIRSTBYTE_LOWEST = 0x81
SJIS_FIRSTBYTE_HIGHEST = 0xEA
SJIS_SECONDBYTE_LOWEST = 0x40
SJIS_SECONDBYTE_HIGHEST = 0xFC

def bytes_to_bits(b):
    return format(b, '08b')

#try our best to create an output ROM that we can edit
def ensure_output_rompath(input_rompath=None, output_rompath=defaults.OUTPUT_ROM):
    """do all we can to make sure we have an output romfile to edit"""
    rom = Path()
    if output_rompath.exists():
        rom = output_rompath
    else:
        if input_rompath is None:
            raise ValueError("No input ROM path provided and output ROM doesn't exist. Put a ROM in ./game or use argument --input_rompath")
        output_rompath.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(input_rompath, output_rompath)
        rom = output_rompath
    return rom

#a bunch of FF is perfect for inserting stuff!
def find_juicy_insert_position(size, start=defaults.BLANKSPACE_STARTPOS, rompath=defaults.OUTPUT_ROM):
    """Find offset of the first `size` bytes all set to 0xFF starting from `start`."""
    all_ff = b'\xff' * size
    with open(rompath, "rb") as f:
        f.seek(start)
        buf = f.read(size)
        offset = start
        while len(buf) == size:
            if buf == all_ff:
                return offset
            next_byte = f.read(1)
            offset += 1
            buf = buf[1:] + next_byte #sliding window - remove 1st byte then append next
    return None
    
    
def get_files(path: Path, extension=None):
    """get all files in a folder + error handling"""
    path.mkdir(parents=True, exist_ok=True)
    if extension:
        try:
            files = [
            f for f in path.iterdir()
            if f.is_file() and f.suffix.lower() == extension
        ]
            if not files:
                    raise ValueError(f"No files in path {path}.")
        except FileNotFoundError:
            raise FileNotFoundError(f"Files in {path} not found. The folder has been created, but needs to be filled with files.")
        except NotADirectoryError:
            raise NotADirectoryError(f"{path} is not a directory.")
        return files
    else:
        try:
            files = [f for f in path.iterdir() if f.is_file()]
            if not files:
                    raise ValueError(f"No files in path {path}.")
        except FileNotFoundError:
            raise FileNotFoundError(f"Files in {path} not found. The folder has been created, but needs to be filled with files.")
        except NotADirectoryError:
            raise NotADirectoryError(f"{path} is not a directory.")
        return files
    
def overwrite_output_rom(source, dest=defaults.OUTPUT_ROM):
    print("overwriting output ROM...")
    if dest.exists():
        dest.unlink() #delete rom
        shutil.copy(source, dest)
    print("Finished!")


def align_bytes_by_4(pos):
    offby = pos % 4
    pass

def is_1byte_sjis(byte):
    if len(byte) != 1:
        return False
    byte = int.from_bytes(byte)
    if byte == 0xa:
        return True
    if byte >= 0x20 and byte <= 0x7e:
        result = True
    return False

def is_2byte_sjis(the_bytes):
    if len(the_bytes) <= 1:
        return False
    byte1_int = the_bytes[0]
    byte2_int = the_bytes[1]
    byte_1_match = True if byte1_int >= SJIS_FIRSTBYTE_LOWEST and byte1_int <= SJIS_FIRSTBYTE_HIGHEST else False
    byte_2_match = True if byte2_int >= SJIS_SECONDBYTE_LOWEST and byte2_int <= SJIS_SECONDBYTE_HIGHEST else False
    if byte_1_match and byte_2_match:
        return True
    return False

def is_sjis(the_bytes):
    if len(the_bytes) == 1:
        return is_1byte_sjis(the_bytes)
    if len(the_bytes) == 2:
        if is_1byte_sjis(bytes(the_bytes[0])):
            return True
        return is_2byte_sjis(the_bytes)
    return False

def create_tbl_dict(tbl_path: Path):
    tbl_dict = {}
    with open(tbl_path, "r") as f:
        for line in f.readlines():
            print(line)
            parts = line.split("=")
            byte = parts[0]
            char = parts[1]
            tbl_dict[byte] = char.strip()
    return tbl_dict
