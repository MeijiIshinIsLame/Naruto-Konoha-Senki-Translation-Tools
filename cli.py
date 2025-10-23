import argparse
from pathlib import Path
from utils import helpers
from config import defaults
from extract.extract_font import extract_chars_and_draw
from extract.extract_entities import extract_entities
from extract.extract_name_labels import extract_name_labels
from extract.extract_menu import extract_menu
from inject.inject_font import inject_font
from inject.inject_dialog_scripts import inject_dialog_scripts
from inject.inject_entities import inject_entities
from inject.inject_name_labels import inject_name_labels
from inject.inject_menu import inject_menu
from inject.inject_asm import prepare_and_inject_asm

def parse_args():
    parser = argparse.ArgumentParser(description="A CLI tool for extracting and injecting files to Naruto Konoha Senki")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    #---------------------------- EXTRACT FONT --------------------------------
    extract_font_parser = subparsers.add_parser("extract_font", help="Extract 1 byte character SJIS font as BMP files to ./extract/font")
    extract_font_parser.add_argument("--rompath", "-i", help="Path of the ROM to extract from. Can be an exact or relative path.")
    extract_font_parser.add_argument("--output_folder", "-o", help="Optional. Path to save font images to. Can be an exact or relative path.")
    extract_font_parser.add_argument("--sjis_table", "-s", help="Optional. Path to the SJIS table file. Can be an exact or relative path.")
    
    #---------------------------- EXTRACT NAMES AND DESCRIPTIONS (items/moves) --------------
    extract_entities_parser = subparsers.add_parser("extract_entities", help="Extract names and descriptions of characters and items to ./extract/entities")
    extract_entities_parser.add_argument("--rompath", "-i", help="Path of the ROM to extract from. Can be an exact or relative path.")
    extract_entities_parser.add_argument("--output_folder", "-o", help="Optional. Path to save font text files to. Can be an exact or relative path.")
    
    #---------------------------- EXTRACT NAME LABELS (character dialog names and places) --------------
    extract_namelabels_parser = subparsers.add_parser("extract_name_labels", help="Extract names of characters and places in dialog scripts to ./extract/name_labels")
    extract_namelabels_parser.add_argument("--rompath", "-i", help="Path of the ROM to extract from. Can be an exact or relative path.")
    extract_namelabels_parser.add_argument("--output_folder", "-o", help="Optional. Path to save font text files to. Can be an exact or relative path.")
    
    #---------------------------- EXTRACT MENU --------------
    extract_menu_parser = subparsers.add_parser("extract_menu", help="Extract menu text to ./extract/menu")
    extract_menu_parser.add_argument("--rompath", "-i", help="Path of the ROM to extract from. Can be an exact or relative path.")
    extract_menu_parser.add_argument("--output_folder", "-o", help="Optional. Path to save font text files to. Can be an exact or relative path.")

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
    
    #---------------------------- INJECT ENTITIES NAMES AND DESCRIPTIONS (items/moves) ---------------------------------
    inject_entities_parser = subparsers.add_parser("inject_entities", help="Takes a folder of entities, convert them to binary, replace their pointers, and insert the pointers + dialogs into ROM.")
    inject_entities_parser.add_argument("--input_rompath", "-i", help="Optional unless there is no output ROM yet. Path of the ROM to copy into the new ROM. Can be an exact or relative path.")
    inject_entities_parser.add_argument("--entities_path", "-f", help="Optional. Path of folder with dialogs to inject. Can be an exact or relative path.")
    inject_entities_parser.add_argument("--output_rompath", "-o", help="Optional unless there is no output ROM yet and no input rompath specified. Path of the output rom file. Can be an exact or relative path.")
    inject_entities_parser.add_argument("--overwrite_output_rom", "-w",  action='store_true', help="Optional. Overwrite output ROM with input ROM.")
    
    #---------------------------- INJECT NAME LABELS (character dialog names and places) ---------------------------------
    inject_namelabels_parser = subparsers.add_parser("inject_name_labels", help="Takes a folder of name labels, and inserts them into ROM")
    inject_namelabels_parser.add_argument("--input_rompath", "-i", help="Optional unless there is no output ROM yet. Path of the ROM to copy into the new ROM. Can be an exact or relative path.")
    inject_namelabels_parser.add_argument("--labels_path", "-f", help="Optional. Path of folder with dialogs to inject. Can be an exact or relative path.")
    inject_namelabels_parser.add_argument("--output_rompath", "-o", help="Optional unless there is no output ROM yet and no input rompath specified. Path of the output rom file. Can be an exact or relative path.")
    inject_namelabels_parser.add_argument("--overwrite_output_rom", "-w",  action='store_true', help="Optional. Overwrite output ROM with input ROM.")
    
    #---------------------------- INJECT MENU ---------------------------------
    inject_menu_parser = subparsers.add_parser("inject_menu", help="Takes a folder of menu items, and inserts them into ROM")
    inject_menu_parser.add_argument("--input_rompath", "-i", help="Optional unless there is no output ROM yet. Path of the ROM to copy into the new ROM. Can be an exact or relative path.")
    inject_menu_parser.add_argument("--labels_path", "-f", help="Optional. Path of folder with dialogs to inject. Can be an exact or relative path.")
    inject_menu_parser.add_argument("--output_rompath", "-o", help="Optional unless there is no output ROM yet and no input rompath specified. Path of the output rom file. Can be an exact or relative path.")
    inject_menu_parser.add_argument("--overwrite_output_rom", "-w",  action='store_true', help="Optional. Overwrite output ROM with input ROM.")

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
        
    if args.command == "extract_entities":
        kwargs = {}
        if args.output_folder:
            kwargs["out_path"] = Path(args.output_folder)
        extract_entities(Path(args.rompath), **kwargs)
        
    if args.command == "extract_name_labels":
        kwargs = {}
        if args.output_folder:
            kwargs["out_path"] = Path(args.output_folder)
        extract_name_labels(Path(args.rompath), **kwargs)
        
    if args.command == "extract_menu":
        kwargs = {}
        if args.output_folder:
            kwargs["out_path"] = Path(args.output_folder)
        extract_menu(Path(args.rompath), **kwargs)

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
        
    if args.command == "inject_entities":
        kwargs = {}
        if args.input_rompath:
            kwargs["input_rompath"] = Path(args.input_rompath)
        if args.entities_path:
            kwargs["entities_path"] = Path(args.entities_path)
        if args.output_rompath:
            kwargs["output_rompath"] = Path(args.output_rompath)
        if args.overwrite_output_rom:
            #try to get output path from kwargs, otherwise use default
            dest = kwargs.get("output_rompath", defaults.OUTPUT_ROM)
            helpers.overwrite_output_rom(source=kwargs["input_rompath"], dest=dest)
        inject_entities(**kwargs)
        
    if args.command == "inject_name_labels":
        kwargs = {}
        if args.input_rompath:
            kwargs["input_rompath"] = Path(args.input_rompath)
        if args.labels_path:
            kwargs["labels_path"] = Path(args.labels_path)
        if args.output_rompath:
            kwargs["output_rompath"] = Path(args.output_rompath)
        if args.overwrite_output_rom:
            #try to get output path from kwargs, otherwise use default
            dest = kwargs.get("output_rompath", defaults.OUTPUT_ROM)
            helpers.overwrite_output_rom(source=kwargs["input_rompath"], dest=dest)
        inject_name_labels(**kwargs)

    if args.command == "inject_menu":
        kwargs = {}
        if args.input_rompath:
            kwargs["input_rompath"] = Path(args.input_rompath)
        if args.labels_path:
            kwargs["labels_path"] = Path(args.labels_path)
        if args.output_rompath:
            kwargs["output_rompath"] = Path(args.output_rompath)
        if args.overwrite_output_rom:
            #try to get output path from kwargs, otherwise use default
            dest = kwargs.get("output_rompath", defaults.OUTPUT_ROM)
            helpers.overwrite_output_rom(source=kwargs["input_rompath"], dest=dest)
        inject_menu(**kwargs)
        
        
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
        inject_entities(**kwargs)
        inject_name_labels(**kwargs)
        inject_menu(**kwargs)
        prepare_and_inject_asm(**kwargs)