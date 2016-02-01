#/usr/bin/env python
import data
import il_parser
import register_allocator
import assembly_generator

from data import debug

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
    debug("Debugging Mode On",b=args.debug)
    il_parser.parse_il(args.file)
    assembly_generator.assembly_generator()
