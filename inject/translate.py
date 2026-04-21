#drop this in a folder to fast edit all the names in the txt files
from pathlib import Path

files = list(Path('.').glob('*.txt'))
i = 0
for file in files:
    oldcontents = ""
    with open(file, "r", encoding="Shift-JIS") as f:
        oldcontents = (f.read())
    i += 1
    newcontents = input(f"{oldcontents}: ")
    if newcontents:
        with open(file, "w", encoding="Shift-JIS") as f:
            f.write(newcontents)
            print(f"{oldcontents} replaced with {newcontents}")