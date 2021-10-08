import argparse
import os

from .converter import Deck

parser = argparse.ArgumentParser(prog="anki_converter", description="Markdown to Anki-compatible CSV files")
parser.add_argument("files", nargs="+", help="File(s) to be converted")
args = parser.parse_args()

for filename in args.files:
    csvname = os.path.splitext(filename)[0]+".csv"
    print(f"Converting {filename} to {csvname}")
    with open(filename) as f:
        deck = Deck()
        deck.parse(f.read())
        deck.write(csvname)