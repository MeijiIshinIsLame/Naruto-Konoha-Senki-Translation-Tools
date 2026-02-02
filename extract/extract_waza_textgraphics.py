import io
import os
import glob
from io import BytesIO
from pathlib import Path
from classes.pointers import Pointer, PointerList
from config import defaults
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageColor

POINTERS_START = 0x5a4ce8
POINTERS_END = 0x5a4de8

palette = {
    0x0: "#32FF4E",
    0x1: "#242828",
    0x2: "#242828",
    0x3: "#302828",
    0x4: "#2C2C2C",
    0x5: "#303030",
    0x6: "#383838",
    0x7: "#444444",
    0x8: "#242424",
    0x9: "#585858",
    0xA: "#585858",
    0xB: "#848888",
    0xC: "#909494",
    0xD: "#909494",
    0xE: "#C0C8C8",
    0xF: "#D8E4E4",
}

def bytes_to_bits(b):
    return format(int.from_bytes(b, byteorder='big'), '08b')

def get_filesize(f):
    original_pos = f.tell()
    f.seek
    size = f.tell()
    f.seek(original_pos)
    return size

def unpack(f, f2):
    magic = f2.read(1)
    print("magic:", magic)
    if magic != b"\x10":
        print("Not LZ77 Compressed!")
        return None
    else:
        unpacked_bytes_length = 0
        buffer_size = int.from_bytes(f2.read(3), byteorder='big')
        print("Buffer Size in bytes:", int(buffer_size))
        if buffer_size < 60000:
            while get_filesize(f) < buffer_size:
                flag = f2.read(1)
                flagbits = bytes_to_bits(flag)
                for bit in flagbits:
                    if bit == "0":
                        f.write(f2.read(1))
                        unpacked_bytes_length += 1
                    elif bit == "1":
                        compression_flags = int.from_bytes(f2.read(2), byteorder='little')
                        n = (compression_flags >> 4) & 0xF
                        length = n + 3
                        disp = ((compression_flags & 0xF) << 8) | (compression_flags >> 8)
                        print(f"length of buffer: {f.tell()} target file buffer length: {f2.tell()} sourcebytes: {hex(compression_flags)}, Length HEX: {hex(n)}, Length INT: {n} disp HEX: {hex(disp)} disp INT: {disp}")
                        read_backbytes(f, length, disp, buffer_size)
                        if get_filesize(f) >= buffer_size:
                            break
        else:
            return None

def read_backbytes(f, length, disp, buffer_size):
    original_pos = f.tell()
    disp = disp + 1
    for i in range(length):
        if f.tell() >= buffer_size:
            break
        f.seek(-disp, 1)
        b = f.read(1)
        f.seek(0, 2)
        f.write(b)

def extract_images(f, folderpath, w=8, h=8):
    tilewidth = 8
    tileheight = 8
    j = 1
    numbytes = int((w * h) / 2)
    while True:
        i = 0
        b = f.read(numbytes)
        if not b:
            break
        colors_per_pixel = []
        img = Image.new("RGB", (w, h))
        pixels = img.load()
        for byte in b:
            right = (byte >> 4) & 0xF
            left = byte & 0xF
            colors_per_pixel.append(palette[left])
            colors_per_pixel.append(palette[right])
        for pixel in colors_per_pixel:
            x = i % tilewidth
            y = i // tileheight
            try:
                pixels[x, y] = ImageColor.getcolor(pixel, "RGB")
            except:
                break
            i+=1
        #img = img.resize((w * 4, h * 4), Image.NEAREST)
        full_filename = Path(folderpath / f"{j}.png")
        img.save(full_filename)
        print(full_filename)
        j += 1

def extract_waza_textgraphics(start=POINTERS_START, end=POINTERS_END, rom=defaults.OUTPUT_ROM):
    ptrs = PointerList(start_addr=start, end_addr=end, rompath=rom)
    with open(rom, "rb") as f:
        for ptr in ptrs:
            print(f"############# {hex(int(ptr))} #############")
            data_start = int(ptr) - 0x08000000
            try:
                f.seek(data_start)
            except:
                print(f"{hex(int(ptr))} is not in ROM")
                continue
            base_path = Path("extract/images") / str(ptr.hex())
            binary_path = Path(base_path / "binary")
            tiles_path = Path(base_path / "tiles")
            letters_path = Path(base_path / "letters")
            assembled_tiles_path = Path(base_path / "assembled_tiles")

            base_path.mkdir(parents=True, exist_ok=True)
            binary_path.mkdir(parents=True, exist_ok=True)
            tiles_path.mkdir(parents=True, exist_ok=True)
            letters_path.mkdir(parents=True, exist_ok=True)
            assembled_tiles_path.mkdir(parents=True, exist_ok=True)
            binfile = Path(binary_path / f"{str(ptr.hex())}.bin")

            b = None
            #binary
            with open(binfile, "w+b") as f2:
                unpack(f2, f)
                b = f2.read()
            #tiles
            with open(binfile, "rb") as f2:
                width = 8
                height = 8
                extract_images(f=f2, folderpath=tiles_path, w=width, h=height)
            #Whole letters
            with open(binfile, "rb") as f2:
                width = 8 * 4
                height = 8 * 4
                extract_images(f=f2, folderpath=letters_path, w=width, h=height)
            #full image (horizontal) - might need to change height to 8 but we'll see
            with open(binfile, "rb") as f2:
                width = get_full_width(b)
                height = 8 * 4
                extract_images(f=f2, folderpath=assembled_tiles_path, w=width, h=height)

def get_full_width(b):
    size = len(b)
    tile_width = 8
    width = size / tile_width
    return width
