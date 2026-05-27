from pathlib import Path

font_path = Path("font_images")
tbl = Path("../../config/custom.tbl")
fontfiles = [
    f for f in font_path.iterdir()
    if f.is_file() and f.suffix.lower() == ".png"
]

tbl_lines = ""
with open(tbl, 'r', encoding="Shift-JIS") as file:
    tbl_lines = file.readlines()
    
for i in range(0, len(tbl_lines)):
    hexval = tbl_lines[i][0:4]
    fontfiles[i].rename(f"{hexval}.png")