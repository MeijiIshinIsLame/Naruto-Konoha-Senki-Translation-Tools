from tqdm import tqdm
from pathlib import Path
from utils import helpers
from config import defaults
from pathlib import Path
from PIL import Image

WHITE = (248, 248, 248)
WHITER = (255, 255, 255)
GREY = (144, 144, 152)
BLACK = (40, 40, 80) #yeah dude I know its technically dark purple OK?

BLACK_2BIT = "11"
GRAY_2BIT = "01"
WHITE_2BIT = "00"

pixel_to_bits = {WHITE: WHITE_2BIT, WHITER: WHITE_2BIT, BLACK: BLACK_2BIT, GREY: GRAY_2BIT}

font_path = Path("inject/vwf/font_images")

class Char:
    def __init__(self, path):
        self.path = path
        self.img = Image.open(path).convert("RGB")
        self.pixels = self.img.load()
        self.width, self.height = self.img.size
        self.sjis = int(self.path.stem, 16)


def make_charlist(font_path):
    chars = []
    fontfiles = [
            f for f in font_path.iterdir()
            if f.is_file() and f.suffix.lower() == ".png"
        ]
    for file in fontfiles:
        chars.append(Char(file))
    return chars

#check if the entire y axis is white bg
def is_all_white_column(char, x):
    for y in range(0, char.height):
        current_pixel = char.pixels[x, y]
        if current_pixel != WHITE:
            return False
    return True

#if its all white bg for the whole y axis and no more black afterwards, the width ends there
def get_charwidth(char):
    if char.path.stem == "899E": return 2 #dont even bother with space cuz its 2 fo sho
    width = char.width
    #start at 1 cuz u cant have a 0 px image
    for x in range(1, char.width):
        x_is_white_y_axis = is_all_white_column(char, x)
        prev_x_is_white_y_axis = is_all_white_column(char, x - 1)
        if x_is_white_y_axis and not prev_x_is_white_y_axis:
            width = x
    return width

def calculate_insert_position(sjis):
    start_address = 0xA2154
    initial_offset = 32 #maybe 32?
    final_offset = initial_offset - sjis
    start = start_address + final_offset
    return start

#chars are compressed to 2bpp little endian in ROM
def compress(char):
    b = bytes()
    for y in range(0, 16):
        bits = []
        byte_pair = []
        for x in range(0, 8):
            pixel = char.pixels[x, y]
            bitpair = pixel_to_bits[pixel]
            bits.append(bitpair)
            if len(bits) == 4:
                byte_pair.append(bits_to_byte(bits))
                bits = []
            if len(byte_pair) == 2:
                b += byte_pair[0]
                b += byte_pair[1]
                byte_pair = []
    return b

def bits_to_byte(bits):
    #in ROM its stored as [R] [L] [R] [L]
    #for example: 11 00 11 00 = W B W B
    #basically, the pairs are swapped. Wow!!
    bitstring = ""
    #yeah i know dude
    bitstring += bits[3]
    bitstring += bits[2]
    bitstring += bits[1]
    bitstring += bits[0]
    byte_value = int(bitstring, 2) 
    b = bytes([byte_value])
    return b


def inject_vwf_font(input_rompath=None, font_path=font_path, output_rompath=defaults.OUTPUT_ROM):
    rom = helpers.ensure_output_rompath(input_rompath, output_rompath)
    chars = make_charlist(font_path)
    start = 0xA2154
    print("Inserting variable width font...")
    for char in tqdm(chars):
        width = bytes([get_charwidth(char)])
        b = compress(char)
        with open(rom, "r+b") as f:
            #mid = len(b) // 2
            #first_half = b[:mid]
            #second_half = b[mid:]
            f.seek(start)
            f.write(width)
            f.write(b)
            #f.write(first_half)
            #f.write(width)
            #f.write(second_half)
        start = start + 64
        print(hex(start))
    print("Finished")