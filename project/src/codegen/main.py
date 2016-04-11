#/usr/bin/env python3
from . import data
from . import il_parser
from . import register_allocator
from . import assembly_generator

from .data import debug

if __name__ == "__main__" :

    import argparse
    parser = argparse.ArgumentParser(description='Generate Assembly Code from 3-instruction code')
    parser.add_argument('file', metavar='file_name', type=argparse.FileType('r'),
                        help='file containing 3-instruction code.')
    parser.add_argument('-d','--debug', dest='debug', action='store_const',
                        const=1, default=0,
                        help='Turn on Debugging.')
    args = parser.parse_args()
    from sys import stderr
    data.debug_flag = args.debug
    debug("Debugging Mode On")
    il_parser.parse_il(args.file)
    assembly_generator.assembly_generator()

def generate_assembly(list_3AC) :
    il_parser.parse_il_from_list(list_3AC)
    assembly_generator.assembly_generator()
