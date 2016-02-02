import register_allocator
import data
from data import debug

def boilerplate() :
    '''Generates Variable space and other directives. '''
    pass


def assembly_generator() :
    '''Entry point for assembly generation after parse_il()'''
    def block_assembly_generator() :
        '''Generates assembly code for current block. '''
        data.numins = len(data.block)
        
        register_allocator.initblock()
        for i in range(0, len(data.block)):
            register_allocator.ini()
            OP_MAP[data.block[i].type](i)
        for line in data.out :
            print (line)

    boilerplate()
    breakpoints = set()
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
        block_assembly_generator()

###  OP_CODE SRC, DEST

def ADD(i) :
    (x, y, z) = (data.block[i].out, data.block[i].in1, data.block[i].in2)
    try :
        int(z)
        data.zprime = z
    except :
        register_allocator.getz(z)
        pass
    register_allocator.getreg(x, y, i)
    try :
        int(y)
        data.yprime = y
    except :
        pass
    register_allocator.gety(y)
    data.out.append("addl " + register_allocator.transform(data.zprime) + ", " + register_allocator.transform(data.L))
    register_allocator.update(x)
    register_allocator.freereg(y, i)
    register_allocator.freereg(z, i)

def SUB(i) :
    (x, y, z) = (data.block[i].out, data.block[i].in1, data.block[i].in2)
    try :
        int(z)
        data.zprime = z
    except :
        register_allocator.getz(z)
        pass
    register_allocator.getreg(x, y, i)
    try :
        int(y)
        data.yprime = y
    except :
        pass
    register_allocator.gety(y)
    data.out.append("subl " + register_allocator.transform(data.zprime) + ", " + register_allocator.transform(data.L))
    register_allocator.update(x)
    register_allocator.freereg(y, i)
    register_allocator.freereg(z, i)

def MUL(i) :
    (x, y, z) = (data.block[i].out, data.block[i].in1, data.block[i].in2)
    try :
        int(z)
        data.zprime = z
    except :
        register_allocator.getz(z)
        pass
    register_allocator.getreg(x, y, i)
    try :
        int(y)
        data.yprime = y
    except :
        pass
    register_allocator.gety(y)
    data.out.append("imul " + register_allocator.transform(data.zprime) + ", " + register_allocator.transform(data.L))
    register_allocator.update(x)
    register_allocator.freereg(y, i)
    register_allocator.freereg(z, i)

def ASSIGN(i) :
    (x, y) = (data.block[i].out, data.block[i].in1)
    register_allocator.getreg(x, y, i)
    try :
        int(y)
        data.yprime = y
    except :
        pass
    register_allocator.gety(y)
    register_allocator.update(x)
    register_allocator.freereg(y, i)

def DIV(i) :
    (x, y, z) = (data.block[i].out, data.block[i].in1, data.block[i].in2)
    register_allocator.push('edx')
    try :
        int(z)
        data.zprime = z
    except :
        if data.adesc[z] == 'eax':
            register_allocator.push(z)
        register_allocator.getz(z)
        pass
    register_allocator.getreg(x, y, i, 'eax')
    try :
        int(y)
        data.yprime = y
    except :
        pass
    register_allocator.gety(y)
    data.out.append("idiv " + register_allocator.transform(data.zprime))
    register_allocator.update(x)
    register_allocator.freereg(y, i)
    register_allocator.freereg(z, i)

OP_MAP = {'+': ADD, '-': SUB, '*': MUL, '=' : ASSIGN,'/' : DIV}
