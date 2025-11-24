import os
import shutil
import subprocess
from pathlib import Path
from tqdm import tqdm
from config import defaults
from utils import helpers

"""
Please, allow me to explain.
This may seem dumb at first, but armips only supports
patching files that are in its own directory.
That is why I'm doing all this weird naming and file copy stuff.
-Quade
"""

asm_folder = Path("inject/asm")

def the_os():
    if os.name == 'nt':
        return "Windows"
    elif os.name == 'posix':
        return "Linux"
    else:
        return "Unknown"

def prepare_asm_files(input_rom=defaults.OUTPUT_ROM.name):
    """ASM files need to have the name of the ROM they're patching to,
       So we write it into the files, and make copies of them as -modified."""
    print("Preparing ASM files...")
    asm_files = helpers.get_files(path=asm_folder, extension=".asm")
    for file in tqdm(asm_files):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("{source}", input_rom)
        content = content.replace("{dest}", "output.gba")
        modified_asm = Path(f"{file.parent}/{file.stem}-modified{file.suffix}")
        print(modified_asm)
        with open(modified_asm, "w", encoding="utf-8") as f:
            f.write(content)
    print("Finished!")
    
def inject_asm_files():
    """Inject ASM files to ROM using armips."""
    print("Injecting ASM...")
    asm_files = helpers.get_files(path=asm_folder, extension=".asm")
    modified_asm_files = [f for f in asm_files if "-modified" in f.name]
    base_cwd = os.getcwd()
    for file in tqdm(modified_asm_files):
        os.chdir(asm_folder)
        #run armips to inject the asm. We need to come back here for teh linux option as well.
        if the_os() == "Windows":
            subprocess.run(["armips.exe", file.name], capture_output=True, text=True, check=True)
        else:
            subprocess.run(["./armips", file.name], capture_output=True, text=True, check=True)
        os.chdir(base_cwd)
    print("Finished!")
    
def delete_modified_asm_files():
    """Delete ASM files with '-modified' in their name."""
    for p in asm_folder.glob("*.asm"):
        if p.is_file() and "-modified" in p.stem:
            p.unlink()

def delete_gba_files():
    for p in asm_folder.glob("*.gba"):
        p.unlink()

def prepare_and_inject_asm(input_rompath=None, output_rompath=defaults.OUTPUT_ROM):
    asm_files = None
    try:
        asm_files = helpers.get_files(path=asm_folder, extension=".asm")
    except ValueError:
        asm_files = None
    if asm_files:
        rom = helpers.ensure_output_rompath(input_rompath, output_rompath)
        shutil.copy(rom, Path(f"inject/asm/{rom.name}"))
        prepare_asm_files(rom.name)
        inject_asm_files()
        delete_modified_asm_files()
        shutil.copy(Path(f"{asm_folder}/output.gba"), rom)
        delete_gba_files()
    else:
        print("skipping ASM injection because there are no ASM files")
