import io
from pathlib import Path
from PIL import Image, ImageDraw

start_address = 0x9CD54

def load_sjis_table(filename=Path("../config/sjis-utf8-1byte.tbl")):
    sjis = {}
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            hv, char = line.split("=")
            sjis[char] = hv
    return sjis

#extract the character bytes from ROM
 def extract_char(f, hv):
    initial_offset = 32
    hv = int(hv, 16)
    final_offset = (hv - initial_offset) << 4
    start = start_address + final_offset
    f.seek(start)
    b = f.read(16)
    return b
    
def draw_image(path, b):
    width = 8
    height = 8
    img = Image.new("RGB", (width, height), "white")
    pixels = img.load()
    byte_to_color = {"11": (0, 0, 0),
                     "01": (128, 128, 128),
                     "00": (255, 255, 255),
                     "10": (0, 0, 0)}
    i = 0
    #how do I convert a byte to binary?
    
def extract_chars_and_draw(in_path, out_path, sjis_tbl):
    pass