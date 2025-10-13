import argparse
from pathlib import Path
from utils import helpers
from config import defaults
from extract.extract_font import extract_chars_and_draw
from inject.inject_font import inject_font
from inject.inject_dialog_scripts import inject_dialog_scripts
from inject.inject_asm import prepare_and_inject_asm

def parse_args():
    parser = argparse.ArgumentParser(description="A CLI tool for extracting and injecting files to Naruto Konoha Senki")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    #---------------------------- EXTRACT FONT --------------------------------
    extract_font_parser = subparsers.add_parser("extract_font", help="Extract 1 byte character SJIS font as BMP files to ./extract/font")
    extract_font_parser.add_argument("rompath", help="Path of the ROM to extract from. Can be an exact or relative path.")
    extract_font_parser.add_argument("--output_folder", "-o", help="Optional. Path to save font images to. Can be an exact or relative path.")
    extract_font_parser.add_argument("--sjis_table", "-s", help="Optional. Path to the SJIS table file. Can be an exact or relative path.")
    
    #---------------------------- INJECT FONT ---------------------------------
    inject_font_parser = subparsers.add_parser("inject_font", help="Takes a folder of 8x8 BMP images with their names as SJIS hex, and overwrites the character graphics in the ROM.")
    inject_font_parser.add_argument("--input_rompath", "-i", help="Optional unless there is no output ROM yet. Path of the ROM to copy into the new ROM. Can be an exact or relative path.")
    inject_font_parser.add_argument("--font_path", "-f", help="Optional. Path of font folder with 8x8 BMP images to inject. Can be an exact or relative path.")
    inject_font_parser.add_argument("--output_rompath", "-o", help="Optional unless there is no output ROM yet and no input rompath specified. Path of the output rom file. Can be an exact or relative path.")
    inject_font_parser.add_argument("--overwrite_output_rom", "-w",  action='store_true', help="Optional. Overwrite output ROM with input ROM.")
    
    #---------------------------- INJECT DIALOGS ---------------------------------
    inject_dialog_parser = subparsers.add_parser("inject_dialogs", help="Takes a folder of dialogs, convert them to binary, replace their pointers, and insert the pointers + dialogs into ROM.")
    inject_dialog_parser.add_argument("--input_rompath", "-i", help="Optional unless there is no output ROM yet. Path of the ROM to copy into the new ROM. Can be an exact or relative path.")
    inject_dialog_parser.add_argument("--scripts_path", "-f", help="Optional. Path of folder with dialogs to inject. Can be an exact or relative path.")
    inject_dialog_parser.add_argument("--output_rompath", "-o", help="Optional unless there is no output ROM yet and no input rompath specified. Path of the output rom file. Can be an exact or relative path.")
    inject_dialog_parser.add_argument("--overwrite_output_rom", "-w",  action='store_true', help="Optional. Overwrite output ROM with input ROM.")
    
    #---------------------------- INJECT ASM ---------------------------------    
    inject_asm_parser = subparsers.add_parser("inject_asm", help="Takes a ROM and patches is with the files located in the 'inject' folder.")
    inject_asm_parser.add_argument("--input_rompath", "-i", help="Optional unless there is no output ROM yet. Path of the ROM to copy into the new ROM. Can be an exact or relative path.")
    inject_asm_parser.add_argument("--output_rompath", "-o", help="Optional unless there is no output ROM yet and no input rompath specified. Path of the output rom file. Can be an exact or relative path.")
    inject_asm_parser.add_argument("--overwrite_output_rom", "-w",  action='store_true', help="Optional. Overwrite output ROM with input ROM.")
    
    #---------------------------- INJECT ALL ---------------------------------
    patch_rom_parser = subparsers.add_parser("patch_rom", help="Takes a ROM and patches is with the files located in the 'inject' folder.")
    patch_rom_parser.add_argument("--input_rompath", "-i", help="Optional unless there is no output ROM yet. Path of the ROM to copy into the new ROM. Can be an exact or relative path.")
    patch_rom_parser.add_argument("--output_rompath", "-o", help="Optional unless there is no output ROM yet and no input rompath specified. Path of the output rom file. Can be an exact or relative path.")
    patch_rom_parser.add_argument("--overwrite_output_rom", "-w",  action='store_true', help="Optional. Overwrite output ROM with input ROM.")
    
    args = parser.parse_args()
    
    #---------------------------- EXTRACTION COMMANDS --------------------------------
    if args.command == "extract_font":
        kwargs = {}
        if args.output_folder:
            kwargs["out_path"] = Path(args.output_folder)
        if args.sjis_table:
            kwargs["sjis_tbl_path"] = Path(args.sjis_table)
        extract_chars_and_draw(args.rompath, **kwargs)
    
    #---------------------------- INJECTION COMMANDS ----------------------------------  
    if args.command == "inject_font":
        kwargs = {}
        if args.input_rompath:
            kwargs["input_rompath"] = Path(args.input_rompath)
        if args.font_path:
            kwargs["font_path"] = Path(args.font_path)
        if args.output_rompath:
            kwargs["output_rompath"] = Path(args.output_rompath)
        if args.overwrite_output_rom:
            #try to get output path from kwargs, otherwise use default
            dest = kwargs.get("output_rompath", defaults.OUTPUT_ROM)
            helpers.overwrite_output_rom(source=kwargs["input_rompath"], dest=dest)
        inject_font(**kwargs)
        
    if args.command == "inject_dialogs":
        kwargs = {}
        if args.input_rompath:
            kwargs["input_rompath"] = Path(args.input_rompath)
        if args.scripts_path:
            kwargs["scripts_path"] = Path(args.scripts_path)
        if args.output_rompath:
            kwargs["output_rompath"] = Path(args.output_rompath)
        if args.overwrite_output_rom:
            #try to get output path from kwargs, otherwise use default
            dest = kwargs.get("output_rompath", defaults.OUTPUT_ROM)
            helpers.overwrite_output_rom(source=kwargs["input_rompath"], dest=dest)
        inject_dialog_scripts(**kwargs)
        
    if args.command == "inject_asm":
        kwargs = {}
        if args.input_rompath:
            kwargs["input_rompath"] = Path(args.input_rompath)
        if args.output_rompath:
            kwargs["output_rompath"] = Path(args.output_rompath)
        if args.overwrite_output_rom:
            #try to get output path from kwargs, otherwise use default
            dest = kwargs.get("output_rompath", defaults.OUTPUT_ROM)
            helpers.overwrite_output_rom(source=kwargs["input_rompath"], dest=dest)
        prepare_and_inject_asm(**kwargs)
        
    if args.command == "patch_rom":
        kwargs = {}
        if args.input_rompath:
            kwargs["input_rompath"] = Path(args.input_rompath)
        if args.output_rompath:
            kwargs["output_rompath"] = Path(args.output_rompath)
        if args.overwrite_output_rom:
            #try to get output path from kwargs, otherwise use default
            dest = kwargs.get("output_rompath", defaults.OUTPUT_ROM)
            helpers.overwrite_output_rom(source=kwargs["input_rompath"], dest=dest)
        #do it all, dawg!
        inject_font(**kwargs)
        inject_dialog_scripts(**kwargs)
        prepare_and_inject_asm(**kwargs)