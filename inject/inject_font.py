import io
import shutil
from pathlib import Path
from utils import helpers

BLACK = "11"
GRAY = "01"
WHITE = "00"

'''
Swap each pair in the list because BMP is left to right starting at the bottom,
but the game renders right to left from bottom.
'''
def swap_pairs(lst):
    swapped = lst[:]
    for i in range(0, len(swapped) - 1, 2):
        swapped[i], swapped[i + 1] = swapped[i + 1], swapped[i]
    return swapped

def convert_bmp_bytes(path):
    #file is always 246 bytes no matter what
    start = 0x36
    end = 0xF5
    bitpairs = []
    
    colorconverter = {
        bytes.fromhex("000000"): BLACK,
        bytes.fromhex("808080"): GRAY,
        bytes.fromhex("FFFFFF"): WHITE
    }
    with open(path, "rb") as f:
        f.seek(start)
        while f.tell() <= end:
            color = f.read(3)
            bitpair = colorconverter[color]
            bitpairs.append(bitpair)
    # reverse the 4 bitpairs before joining. The binary is read kinda like little endian.
    binary = [
        "".join(bitpairs[i:i+4][::-1])
        for i in range(0, len(bitpairs), 4)
    ]
    # now that the bytes are created, it must be reversed and pair swapped to render right to left
    flipped = swap_pairs(binary[::-1])
    byte_data = bytes(int(b, 2) for b in flipped) #make it a single bytes object so we can shove it in the ROM.
    return byte_data
    
def calculate_insert_position(sjis):
    start_address = 0x9CD54
    initial_offset = 32
    final_offset = (sjis - initial_offset) << 4
    start = start_address + final_offset
    return start
    
def inject_font(
    input_rompath=None,
    font_path=Path("inject/font"),
    output_rompath=Path("game/Naruto - Konoha Senki English translation.gba")
):
    try:
        fontfiles = [
            f for f in font_path.iterdir()
            if f.is_file() and f.suffix.lower() == ".bmp"
        ]
        if not fontfiles:
            raise ValueError(f"No BMP files in font path {font_path}. Each character needs to be a 8x8 BMP image.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Font folder {font_path} not found.")
    except NotADirectoryError:
        raise NotADirectoryError(f"{font_path} is not a directory.")
        
    rom = helpers.ensure_output_rompath(input_rompath, output_rompath)
        
    for fontfile in fontfiles:
        b = convert_bmp_bytes(fontfile)
        sjis = int(fontfile.stem, 16)
        start = calculate_insert_position(sjis)
        print(f"inserting {hex(sjis)} at 0x{hex(start)}")
        with open(rom, "r+b") as f:
            f.seek(start)
            f.write(b)
    print("Finished")
    
        