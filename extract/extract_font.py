import io
from pathlib import Path
from PIL import Image, ImageDraw

def load_sjis_table(filename=Path("../config/sjis-utf8-1byte.tbl")):
    sjis = {}
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            hv, char = line.split("=")
            sjis[hv] = char
    return sjis

#extract the character bytes from ROM
 def extract_char_bytes(f, hv):
    start_address = 0x9CD54
    initial_offset = 32
    hv = int(hv, 16)
    final_offset = (hv - initial_offset) << 4
    start = start_address + final_offset
    f.seek(start)
    b = f.read(16)
    return b

#draw image of character from charbytes
def draw_image(path, b):
    width = 8
    height = 8
    img = Image.new("RGB", (width, height), "white")
    pixels = img.load()
    byte_to_color = {"11": (0, 0, 0),
                     "01": (128, 128, 128),
                     "00": (255, 255, 255),
                     "10": (0, 0, 0)}
    for i, one_byte in enumerate(b):
        eight_bits = one_byte
        bits = f"{one_byte:08b}"
        rev_bits = bits[::-1] #reversing because its loaded backwards
        chunks = [rev_bits[:2],
                  rev_bits[2:4],
                  rev_bits[4:6],
                  rev_bits[6:8]]
        for bpair in chunks:
            x = i % width
            y = i // width
            pixels[x, y] = byte_to_color[bpair]
    img.save(path)   
        
'''
Extract all chars and save to folder as separate images
'''
def extract_chars_and_draw(game_path,
                           out_path=Path("font"),
                           sjis_tbl_path=Path("../config/sjis-utf8-1byte.tbl")):
    out_path.mkdir(parents=True, exist_ok=True)
    sjis = load_sjis_table(sjis_tbl_path)
    with open(game_path, rb) as f:
        for k, v in enumerate(sjis):
            print(f"Extracting sjis {k} as {v}...")
            b = extract_char_bytes(f, k)
            draw_image(Path(out_path) / f"{k}.bmp", b)
            print("Extraction Complete!")
    print("Finished!")
        
            