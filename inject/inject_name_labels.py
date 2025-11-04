import io
from pathlib import Path
from tqdm import tqdm
from classes.pointers import Pointer, PointerList
from config import defaults
from utils import helpers

EXIT_BYTE = b'\x00'

def get_sjis_and_zeros(f):
    """get a bytes object of SJIS and zeros per name"""
    b = f.read(1)
    data = b
    while b != EXIT_BYTE:
        data += b
        b = f.read(1)
    while b == EXIT_BYTE:
        data += b
        b = f.read(1)
    return data


def inject_name_labels(input_rompath=None, output_rompath=defaults.OUTPUT_ROM, files=Path("inject/name_labels")):
    """check if name bytes can be injected without disruptig offset,
       then inject."""
    print("Inserting Name Labels")
    rom = helpers.ensure_output_rompath(input_rompath, output_rompath)
    files = helpers.get_files(files, ".txt")
    files = sorted(files, key=lambda f: int(Path(f).stem, 16))
    with open(rom, "r+b") as f:
        for i, file in enumerate(tqdm(files)):
            start = int(file.stem, 16)
            f.seek(start)
            maxlen = len(get_sjis_and_zeros(f))
            filesize = file.stat().st_size
            if filesize <= maxlen:
                f.seek(start)
                with open(file, "rb") as f2:
                    data = f2.read()
                    zeros = EXIT_BYTE * (maxlen - len(data) - 1)
                    data += zeros
                    f.write(data)
            else:
                print(f"File {file.stem} cannot be written because it is too long\n filesize: {filesize}, maxlen: {maxlen}")


