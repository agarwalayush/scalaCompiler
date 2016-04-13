import register_allocator
import data
from data import debug

def boilerplate() :
    '''Generates Variable space and other directives. '''
    print(".section .data")
    for v in data.globmap :
        print("{}:".format(v))
        print("\t.long {}".format(1))
    for v in data.arrayset.keys():
        print("{}:".format(v))
        print("\t.zero {}".format(4*int(data.arrayset[v])))
    print("\n.section .text\n")
    for k,v in data.stringMap.items() :
        print('\n'+k+':  .asciz ' +v)
    print('\nprintFormat:  .asciz "%d"')
    print('\nscanFormat:  .asciz "%d"\n')
    print('.global main\n')
    print('main:')
    pass


def programEnd():
    print("\tret")


def assembly_generator() :
    '''Entry point for assembly generation after parse_il()'''
    debug(memmap=data.memmap)
    debug(globmap=data.globmap)
    def block_assembly_generator() :
        '''Generates assembly code for current block. '''
        data.numins = len(data.block)
        debug(numins = data.numins)
        register_allocator.initblock()
        data.print_symbol_table()
        for i in range(0, len(data.block) - 1):
            register_allocator.ini()
            OP_MAP[data.block[i].type](i)
        i = len(data.block) - 1
        if i == -1: return
        if data.block[i].type in {'call', 'ret', 'goto', 'jg', 'je', 'jle', 'jge', 'je', 'jne'}:
            register_allocator.save_to_memory()
            register_allocator.ini()
            OP_MAP[data.block[i].type](i)
        else :
            register_allocator.ini()
            OP_MAP[data.block[i].type](i)
            register_allocator.save_to_memory()
        for line in data.out :
            print ("\t" + line)

    boilerplate()
    breakpoints = set()
    breakpoints.add(0)
    for i in range(0,len(data.raw)) :
        if data.raw[i].type == 'label' :
            breakpoints.add(i)
        if data.raw[i].type in ['call', 'ret', 'goto', 'jg', 'je', 'jle', 'jge', 'je', 'jne']:
            breakpoints.add(i+1)
    breakpoints.add(len(data.raw))
    breakpoints = sorted(breakpoints)
    for i in range(0,len(breakpoints)-1) :
        data.out.clear()
        if data.raw[breakpoints[i]].type == 'cmp' :
            debug(data.raw[breakpoints[i]])
        if data.raw[breakpoints[i]].type == 'label':
            print("\n{}:".format(data.raw[breakpoints[i]].out))
            if data.raw[breakpoints[i]].out.startswith('func') :
                data.curr_scope =  data.raw[breakpoints[i]].out
                print("\t" + "pushl %ebp")
                print("\t" + "movl %esp, %ebp")
                print("\t" + "subl ${}, %esp".format(data.num_var[data.raw[breakpoints[i]].out] - 4))
        if i==0:
           data.block = data.raw[breakpoints[i]:breakpoints[i+1]]
        else:
            if data.raw[breakpoints[i]].type == 'label':
                data.block = data.raw[breakpoints[i] + 1:breakpoints[i+1]]
            else:
                data.block = data.raw[breakpoints[i]:breakpoints[i+1]]
        block_assembly_generator()
#        programEnd()


###  OP_CODE SRC, DEST
def ARG(i) :
    pass

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
    data.out.append("xor %edx, %edx")
    try :
        int(z)
        reg = register_allocator.empty_reg(['edx', 'eax'], i)
        data.out.append('mov $' + z + ", %" + reg)
        data.zprime = reg
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
    data.out.append("idivl " + register_allocator.transform(data.zprime))
    register_allocator.update(x)
    register_allocator.freereg(y, i)
    register_allocator.freereg(z, i)

def MOD(i):
    (x, y, z) = (data.block[i].out, data.block[i].in1, data.block[i].in2)
    register_allocator.push('edx')
    data.out.append("xor %edx, %edx")
    try :
        int(z)
        data.zprime = z
        reg = register_allocator.empty_reg(i,['eax', 'edx'])
        data.out.append('mov $' + z + ", %" + reg)
        data.zprime = reg

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
    data.out.append("idivl " + register_allocator.transform(data.zprime))
    data.L = 'edx'
    register_allocator.update(x)
    register_allocator.freereg(y, i)
    register_allocator.freereg(z, i)

def AND(i):
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
    data.out.append("and " + register_allocator.transform(data.zprime) + ", " + register_allocator.transform(data.L))
    register_allocator.update(x)
    register_allocator.freereg(y, i)
    register_allocator.freereg(z, i)

def OR(i):
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
    data.out.append("or " + register_allocator.transform(data.zprime) + ", " + register_allocator.transform(data.L))
    register_allocator.update(x)
    register_allocator.freereg(y, i)
    register_allocator.freereg(z, i)

def XOR(i):
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
    data.out.append("xor " + register_allocator.transform(data.zprime) + ", " + register_allocator.transform(data.L))
    register_allocator.update(x)
    register_allocator.freereg(y, i)
    register_allocator.freereg(z, i)

def RETURN(i) :
    if data.block[i].out != None :
        data.out.append("movl {}, %eax".format(register_allocator.transform(data.block[i].out)))
    data.out.append("movl %ebp, %esp")
    data.out.append("popl %ebp")
    data.out.append('ret')
    data.out.append('\n')
    data.curr_scope = ""

def CALL(i) :
    data.out.append('call ' + data.block[i].out)
    data.out.append('addl ${}, %esp'.format(data.num_arg[data.block[i].out]-8))


def PRINT(i):
    x = data.block[i].out
    debug(x = x)
    try :
        debug(adesc = data.adesc[x])
        data.adesc[x]
        data.out.append('pushl %' + data.adesc[x])
    except :
        data.out.append('pushl ' + register_allocator.transform(x))
    data.out.append('pushl $printFormat')
    register_allocator.save_to_memory()
    data.out.append('call printf')
    data.out.append('addl $8, %esp')

def READ(i):
    x = data.block[i].out
    data.out.append('pushl $' + x)
    data.out.append('pushl $scanFormat')
    register_allocator.save_to_memory()
    data.out.append('call scanf')
    data.out.append('addl $8, %esp')

def GOTO(i):
    data.out.append('jmp ' + data.block[i].out)

def DEC(i):
    pass

def LOAD_ARRAY(i):
    (x, y, z) = (data.block[i].out, data.block[i].in1, data.block[i].in2)
    k = register_allocator.empty_reg(i)
    try :
        int(z)
        pass
    except :
        register_allocator.getz(z)
    if data.zprime == None:
        data.zprime = z
    data.out.append("movl " + register_allocator.transform(data.zprime) + ", " + register_allocator.transform(k))
    data.L = k
    data.out.append("movl " + y + "(, %" + k + ", 4), %" + k)
    register_allocator.update(x)

def STORE_ARRAY(i):
    (x, y, z) = (data.block[i].out, data.block[i].in1, data.block[i].in2)
    try :
        int(z)
        pass
    except :
        register_allocator.getz(z)
    if data.zprime == None:
        data.zprime = z
    data.out.append("movl " + register_allocator.transform(data.zprime) + ", %edi")

    try :
        int(x)
        data.out.append("movl $" + x + ", " + y + "(, %edi, 4)")
        return
    except :
        pass
   # debug(adesc = data.adesc[x])
    register_allocator.getreg(x, y, i)
    debug(Lp = data.L)
    if data.rdesc[data.L] == None:
        data.out.append("movl " + register_allocator.transform(x) + ", " + register_allocator.transform(data.L))
    data.out.append("movl " + register_allocator.transform(data.L) + ", " + y + "(, %edi, 4)")
    data.adesc[x] = data.L
    data.rdesc[data.L] = x

def PRINT_STR(i):
    inno = data.block[i].no
    data.out.append('pushl $'  + 'str'+ str(inno))
    register_allocator.save_to_memory()
    data.out.append('call printf')
    data.out.append('addl $4, %esp')

def COMPARE(i):
    (y,z) = (data.block[i].in1, data.block[i].in2)
    try:
            int(z)
            data.zprime = z
    except:
        register_allocator.getz(z)

    try:
        int(y)
        data.L = y
    except:
        # print("------------" + data.adesc[y])
        if data.zprime in data.vset and data.adesc[y] == None:
            temp = register_allocator.empty_reg(i,[])
            data.out.append("movl " + register_allocator.transform(y) + ", " + register_allocator.transform(temp))
            data.adesc[y] = temp
            data.rdesc[temp] = y
            data.L = temp
        elif data.adesc[y] != None:
            data.L = data.adesc[y]
        else:
            data.L = y
    data.out.append("cmp " + register_allocator.transform(data.zprime) + "," + register_allocator.transform(data.L))
    register_allocator.freereg(z, i)
    register_allocator.freereg(y, i)

def JE(i):
    data.out.append("je " + data.block[i].out)

def JLE(i):
    data.out.append("jle " + data.block[i].out)

def JGE(i):
    data.out.append("jge " + data.block[i].out)

def JG(i):
    data.out.append("jg " + data.block[i].out)

def JL(i):
    data.out.append("jl " + data.block[i].out)

def JNE(i):
    data.out.append("jne " + data.block[i].out)

def check_variable(var_bar) :
    try :
        int(var_bar)
        return False
    except:
        return True


def PUSH_ARG(i) :
    var = data.block[i].out
    if check_variable(var) and data.adesc[var] != None :
        place = data.adesc[var]
    else :
        place = register_allocator.empty_reg(var)
        data.out.append("movl  " + register_allocator.transform(var) +', ' +  register_allocator.transform(place))
        data.rdesc[place] = var
    data.out.append("pushl %" + place)
    pass

def LABEL(i) :
    pass


OP_MAP = {'+': ADD, '-': SUB, '*': MUL, '=' : ASSIGN,'/' : DIV, '%' : MOD, '^' : XOR, '&' : AND, '|' : OR, 'ret' : RETURN, 'call' : CALL, 'print' : PRINT, 'read' : READ, 'goto' : GOTO, '<-' : LOAD_ARRAY, '->' : STORE_ARRAY, 'array' : DEC, 'printstr': PRINT_STR, 'cmp': COMPARE, 'jl': JL, 'je': JE, 'jg':JG, 'jle':JLE, 'jge':JGE, 'jne':JNE, 'pusharg':  PUSH_ARG, 'arg' : ARG, 'label' : LABEL}
