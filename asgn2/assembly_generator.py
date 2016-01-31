from  register_allocator import *
import data


def boilerplate() :
    '''Generates Variable space and other directives. Takes no argument and uses data from classes.py'''
    pass


def assembly_generator() :
    '''Entry point for assembly generation after parse_il()'''
    def block_assembly_generator() :
        '''Generates assembly code for current block. Takes no argument and uses data from classes.py'''
        data.numins = len(data.block)
        initblock()
        data.print_symbol_table()

    boilerplate()
    breakpoints = set()
    goto_points = {}
    breakpoints.add(0)
    for i in range(0,len(data.raw)) :
        if data.raw[i].type == 'label' :
            breakpoints.add(i)
        if data.raw[i].type == 'goto' :
            breakpoints.add(i+1)
            breakpoints.add(int(data.raw[i].out)-1)
        if data.raw[i].type == 'call' :
            breakpoints.add(i+1)
        if data.raw[i].type == 'ret' :
            breakpoints.add(i + 1)
    breakpoints.add(len(data.raw))
    breakpoints = sorted(breakpoints)
    for i in range(0,len(breakpoints)-1) :
        if i == 0 : data.out.append("_start :")
        elif data.raw[i].type == 'label' : data.out.append("{}:\n".format(data.raw[i].out))
        data.block = data.raw[breakpoints[i]:breakpoints[i+1]]
        print(data.block)
        block_assembly_generator()
