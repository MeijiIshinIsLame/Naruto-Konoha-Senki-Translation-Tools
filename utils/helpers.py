import io
import shutil
from pathlib import Path
from config import defaults

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