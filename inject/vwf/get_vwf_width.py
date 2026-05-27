from pathlib import Path
from PIL import Image

whiteBG = (248, 248, 248)
font_path = Path("font_images")
config_path = Path("config.txt")

class Char:
    def __init__(self, path):
        self.path = path
        self.img = Image.open(path).convert("RGB")
        self.pixels = self.img.load()
        self.width, self.height = self.img.size

#check if the entire y axis is white bg
def is_all_white_column(char, x):
    for y in range(0, char.height):
        current_pixel = char.pixels[x, y]
        if current_pixel != whiteBG:
            return False
    return True

def get_charwidth(char):
    if char.path.stem == "space": return 2 #dont even bother with space cuz its 2 fo sho
    width = char.width
    #start at 1 cuz u cant have a 0 px image
    for x in range(1, char.width):
        x_is_white_y_axis = is_all_white_column(char, x)
        prev_x_is_white_y_axis = is_all_white_column(char, x - 1)
        if x_is_white_y_axis and not prev_x_is_white_y_axis:
            width = x
    return width

def configure_widths(font_path, config):
    #clear config file
    with open(config, 'w') as f:
        pass

    fontfiles = [
            f for f in font_path.iterdir()
            if f.is_file() and f.suffix.lower() == ".png"
        ]
    for file in fontfiles:
        char = Char(file)
        width = get_charwidth(char)
        with open(config, 'a') as f:
            f.write(f"{file}: {width}\n")

configure_widths(font_path, config_path)