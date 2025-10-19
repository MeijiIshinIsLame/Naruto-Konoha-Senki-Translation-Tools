import io
from pathlib import Path
from tqdm import tqdm
from classes.pointers import Pointer, PointerList

START = 0x599280
END = 0x599924 #possibly 24 check after
EXIT_BYTE = b'\x00'

def read_ptrdata(f, ptr):
    ptrloc = f.tell()
    f.seek(int(ptr) - 0x08000000)
    b = read_until(f, EXIT_BYTE)
    f.seek(ptrloc)
    return b

def read_until(f, exit_byte=EXIT_BYTE):
    b = f.read(1)
    the_bytes = bytes()
    while b != exit_byte:
        the_bytes += b
        b = f.read(1)
    return the_bytes

def extract_entities(input_rompath, output_folder=Path("extract/entities")):
    print("Extracting Entities...")
    output_folder.mkdir(parents=True, exist_ok=True)
    ptrs = PointerList(start_addr=START, end_addr=END, rompath=input_rompath)
    with open(input_rompath, "rb") as f:
        for ptr in tqdm(ptrs):
            if int(ptr) > 0x08000000:
                b = read_ptrdata(f, ptr)
                out_path = Path(f"{output_folder}/{str(hex(int(ptr)))}.txt")
                with open(out_path, "w", encoding="shift-jis") as fout:
                    decoded_text = b.decode('shift-jis', errors='replace')
                    fout.write(decoded_text)
    print("Finished!")