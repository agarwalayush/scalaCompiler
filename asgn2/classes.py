#This file contains global data structures that are refreshed after each basic block

import sys

#class for the parsed instructions, add type, target for extra fuinctionality
class instruction3ac :
    def __init__(self, no, type, in1, in2, out) :
        self.no, self.type, self.in1, self.in2, self.out, no, type, in1, in2, out


#raw is a list of the parsed instructions
#block is a list of instructions corresdonding to a basic block
#TODO : a block generator, which builds the global data structures block, symtable and clears address and register descriptors

raw = []
block = []

#vset[] is a set of all the variables of the program. To be used in the .data section
vset = set()

#rset is a list of all the general purpose registers
rset = ['eax', 'ebx', 'ecx', 'edx', 'esi', 'edi']

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

def fillblock(startinstruction):
    #fill the block[] and update numins
    #return the target instruction number for the next blocks
    return (insno1, insno2)

def initblock():
    #builds the symtable[] once block[] and numins are filled and initializes other data structures
    rdesc.clear()
    for x in rset:
        rdesc[x] = None

    adesc.clear()
    for x in vset.keys():
        adesc[x] = None

    out.clear()

    symtable.clear()
    for x in range(0, numins):
        for y in vset.keys():
            symtable[x][y] = INF

    #scan from backwards to set the live ranges assuming all variables to be dead on exit
    i = numins - 1
    while(i > 0):
        (x, y, z) = (block[i].out, block[i].in1, block[i].in2)
        for k in vset.keys():
            if k == y or k == z :
                symtable[i - 1][k] = i
            elif k != x:
                symtable[i - 1][k] = symtable[i][k]
        i = i - 1

#This function transforms a memory location to include the sqaure brackets
def transform(str):
    if str in rset :
        return str
    else:
        return "[" + str + "]"

#This function initializes some global variables

def ini():
    L = None
    yprime = None
    zprime = None
