from pathlib import Path

START = 0x408B80
END = 0x408BD6
EXIT_BYTE = b'\x00'
extract_path = Path("extract/menu")
extract_path.mkdir(parents=True, exist_ok=True)

def extract_menu(rom, extract_path=extract_path):
    """Read all non-zero bytes as SJIS and save in txt files
       with their position in ROM as the filename."""
    print("Extracting Menu Text...")
    with open(rom, 'rb') as f:
        f.seek(START)
        while f.tell() <= END:
            b = f.read(1)
            data = bytes()
            #if we hit sjis we put it in
            while b != EXIT_BYTE:
                data += b
                b = f.read(1)
            if data:
                filename = Path(f"{extract_path}/{hex(f.tell() - len(data) - 1)}.txt")
                with open(filename, "wb") as f2:
                    f2.write(data)
    print("Finished!")