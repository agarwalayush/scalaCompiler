import argparse

parser = argparse.ArgumentParser(description='end-to-end scala compiler')
parser.add_argument('-c','--3ac-only', help='Generate only 3 Address code', action='store_true', default = False)
parser.add_argument('-f','--parsetree-html', help='Generate html parse tree.', action='store_true', default = False)
parser.add_argument('filename')
args = parser.parse_args()
print(args)

from codegen.main import generate_assembly
from lexpar.parser import parse_file
