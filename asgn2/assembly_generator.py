import register_allocator
import data


def boilerplate() :
    '''Generates Variable space and other directives. Takes no argument and uses data from classes.py'''
    pass


def assembly_generator() :
    '''Entry point for assembly generation after parse_il()'''
    def block_assembly_generator() :
        '''Generates assembly code for current block. Takes no argument and uses data from classes.py'''
        data.numins = len(data.block)
        register_allocator.initblock()
        data.print_symbol_table()
        for i in range(0, len(data.block)):
            register_allocator.ini()
            (x, y, z, op) = (data.block[i].out, data.block[i].in1, data.block[i].in2, data.block[i].type)
#            print ("test", data.adesc[y])
            register_allocator.getz(z)
            register_allocator.getreg(x, y, i, 1)
            register_allocator.gety(y)
            data.out.append("ADDL " + register_allocator.transform(data.L) + ", " + register_allocator.transform(data.zprime))
            register_allocator.update(x)
            register_allocator.freereg(y, i)
            register_allocator.freereg(z, i)
            print(data.adesc)
            print(data.rdesc)
            print(data.debug)
#        for k in data.vset:
 #           if data.adesc[k] != None :
  #              register_allocator.push(data.adesc[k])
  
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
        print(data.block)
        block_assembly_generator()
