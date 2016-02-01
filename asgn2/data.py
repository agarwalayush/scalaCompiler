#class for the parsed instructions, add type, target for extra fuinctionality
class instruction3ac :
    def __init__(self, no, type, in1, in2, out) :
        self.no, self.type, self.in1, self.in2, self.out = no, type, in1, in2, out
    def __str__(self) :
        return "Instruction No :{},Instruction Type :{}".format(self.no,self.type)
    def __repr__(self) :
        return "\n{}. {} {} {} {} ".format(self.no,self.out, self.type, self.in1, self.in2)


#raw is a list of the parsed instructions
#block is a list of instructions corresdonding to a basic block
#TODO : a block generator, which builds the global data structures block, symtable and clears address and register descriptors

raw = []
block = []

#vset[] is a set of all the variables of the program. To be used in the .data section
vset = set()

#rset is a list of all the general purpose registers
rset = ['eax', 'ebx', 'ecx', 'edx']

#symtable[] is a list st symtable[instruction_no.]<var : nextuse>. nextuse = INF means that the variable is dead
symtable = []

#address descriptor adesc{} is a dictionary st adesc[var] = Register containing var.
# note that each variable will be contained in atmost 1 register. adesc[var] == None implies that no register contains var
# and thus var should be present in memory
adesc = {}

#register descriptor rdesc{} is a dictionary st rdesc[reg] = var st reg currently holds the correct value of the "live" variable
#var. Note that a register can contain atmost 1 variable. rdesc[reg] = None implies that the register is free.
rdesc = {}

#list of string to store the output of the block
out = []


#Total number of instructions, the registers zprime, yprime and L used in register allocation
numins = 0
zprime = None
yprime = None
L = None


def print_symbol_table() :
    s = [[str(e) for e in row.values()] for row in symtable]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '  '.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('-'*(sum(lens)+len(lens)*2)+'|')
    print(fmt.format(*adesc),'|')
    print('-'*(sum(lens)+len(lens)*2)+'|')
    print('  |\n'.join(table),' |')

debug_flag = 0

def debug(*arg,**kwarg) :
    if debug_flag :
         print('\033[91m',)
         for a in arg :
             print(a,end=', ')
         for k,v in kwarg.items() :
             print(k,'=',v,end=', ')
         print('\033[0m')
