import argparse
from pathlib import Path
from extract.extract_font import extract_chars_and_draw

def parse_args():
    parser = argparse.ArgumentParser(description="A CLI tool for extracting and injecting files to Naruto Konoha Senki")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    #font extraction
    extract_font_parser = subparsers.add_parser("extract_font", help="Extract 1 byte character SJIS font as BMP files to ./extract/font")
    extract_font_parser.add_argument("rompath", help="Path of the ROM to extract from. Can be an exact or relative path.", required=True)
    extract_font_parser.add_argument("--output_folder", "-o", help="Path to save font images to. Can be an exact or relative path. Optional argument.")
    extract_font_parser.add_argument("--sjis_table", "-s", help="Path to the SJIS table file. Can be an exact or relative path. Optional argument.")
    
    args = parser.parse_args()
    
    if args.command == "extract_font":
        out_path = Path(args.output_folder) if args.output_folder else None
        sjis_tbl_path = Path(args.sjis_table) if args.sjis_table else None
        extract_chars_and_draw(args.rompath, out_path=out_path, sjis_tbl_path=sjis_tbl_path)