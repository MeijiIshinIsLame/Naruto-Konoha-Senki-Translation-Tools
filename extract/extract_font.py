import io
import shutil
from pathlib import Path
from PIL import Image, ImageDraw

BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)

def load_sjis_table(path=Path("config/sjis-utf8-1byte.tbl")):
    sjis = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                hv, char = line.split("=", 1)
                sjis[hv] = char
            except ValueError:
                print(f"ValueError: skipping {line}")
    return sjis

#extract the character bytes from ROM
def extract_char_bytes(f, hv):
    start_address = 0x9CD54
    initial_offset = 32
    hv = int(hv, 16)
    final_offset = (hv - initial_offset) << 4
    start = start_address + final_offset
    f.seek(start)
    return f.read(16)

#draw image of character from charbytes
def draw_image(path, b):
    width = 8
    height = 8
    img = Image.new("RGB", (width, height), "white")
    pixels = img.load()
    byte_to_color = {
        "11": BLACK,
        "01": GRAY,
        "00": WHITE,
        "10": BLACK
    }
    i = 0
    for one_byte in b:
        eight_bits = one_byte
        bits = f"{one_byte:08b}"
        chunks = [
            bits[:2],
            bits[2:4],
            bits[4:6],
            bits[6:8]
        ]
        chunks = list(reversed(chunks))
        for bpair in chunks:
            x = i % width
            y = i // width
            pixels[x, y] = byte_to_color[bpair]
            i+=1
    img.save(path)   
        
'''
Extract all chars and save to folder as separate images
'''
def extract_chars_and_draw(game_path, out_path=Path("extract/font"), sjis_tbl_path=Path("config/sjis-utf8-1byte.tbl")):
    out_path.mkdir(parents=True, exist_ok=True)
    sjis = load_sjis_table(sjis_tbl_path)
    with open(game_path, "rb") as f:
        for k, v in sjis.items():
            print(f"Extracting sjis {k} as {v}...")
            b = extract_char_bytes(f, k)
            #with open(Path(out_path) / f"{k}.bin", "wb") as f2: f2.write(b)
            draw_image(Path(out_path) / f"{k}.bmp", b)
            print("Extraction Complete!")
    print("Finished!")
        
            