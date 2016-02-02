import data
import math
from data import debug

def initblock():
    #builds the symtable[] once block[] and numins are filled and initializes other data structures
    data.rdesc.clear()
    for x in data.rset:
        data.rdesc[x] = None

    data.adesc.clear()
    for x in data.vset :
        data.adesc[x] = None

    data.out.clear()


    #symtable = [{}]*numins
    data.symtable.clear()
    for x in range(0, data.numins-1):
        data.symtable.append({})
        for y in data.vset :
            data.symtable[x][y] = math.inf
    data.symtable.append({})
    for y in data.vset :
        data.symtable[data.numins-1][y] = data.numins-1


    #scan from backwards to set the live ranges assuming all variables to be dead on exit
    i = data.numins - 1
    while(i > 0):
        (x, y, z) = (data.block[i].out, data.block[i].in1, data.block[i].in2)
        for k in data.vset :
            if k == y or k == z :
                data.symtable[i - 1][k] = i
            elif k != x:
                data.symtable[i - 1][k] = data.symtable[i][k]
        i = i - 1

#This function transforms a memory location to include the sqaure brackets
def transform(st):
    try :
        int(st)
        return '$'+str(st)
    except :
        if st in data.rset :
            return '%'+st
        else:
            return str(st)

#This function initializes some global variables

def ini():
    data.L = None
    data.yprime = None
    data.zprime = None



# This function pushes the variable stored at "reg" into memory and frees it 
def push(register):
    if data.rdesc[register] != None :
        data.out.append("movl %{}, {}".format(register, data.rdesc[register]))
        data.adesc[data.rdesc[register]] = None
        data.rdesc[register] = None

#This function takes a variable var and assigns zprime
def getz(var):
    if var in data.vset : 
        if data.adesc[var] != None:
            data.zprime = data.adesc[var]
        else:
            data.zprime = var

#This function takes variables x, y and the current instruction number returns a suitable memory location / register L
#special: register is given when a particular register is needed, like eax for division
#flag: 1 if there is a constraint on atmost 1 on zprime and L to be a memory location, else 0

def getreg(x, y, ino,special = None):
    if special != None :
        data.L = special
    elif y in data.vset and data.adesc[y] != None and data.symtable[ino][y] == math.inf:
        data.L = data.adesc[y]
    elif data.adesc[x] != None:
        data.L = data.adesc[x]
    if data.L == None:
        for k in data.rset:
            if data.rdesc[k] == None:
                data.L = k
    if data.L == None :
        if(data.symtable[ino][x] != math.inf or (data.zprime not in data.rset)):
           nxtuse = -1
           for k in data.rset:
               if k == data.zprime :
                   continue
               if nxtuse < data.symtable[ino][data.rdesc[k]]:
                   data.L = k
                   nxtuse = data.symtable[ino][data.rdesc[k]]
        else:
            data.L = x
    if data.L in data.rset and data.rdesc[data.L] != None:
        push(data.L)

#This function gives Y' and moves Y' to L if value of Y is not already in L
def gety(var):
    if var in data.vset :
        if data.adesc[var] != None:
            data.yprime = data.adesc[var]
        else:
            data.yprime = var
    if data.yprime != data.L :
        data.out.append("movl " + transform(data.yprime) + ", " + transform(data.L))


                #This function frees a register if the variable it stores becomes dead
#TODO: handle the global variable
def freereg(var, ino):
    if var in data.vset :
        if data.symtable[ino][var] == math.inf and data.adesc[var] != None:
            data.rdesc[data.adesc[var]] = None
            data.adesc[var] = None

#This function updates the address descriptor corresdonding to the out variable
def update(x):
    if data.L in data.rset:
        data.adesc[x] = data.L
        data.rdesc[data.L] = x
    else:
        data.adesc[x] = None
    for v in data.vset :
        if data.adesc[v] == data.L and v != x:
            data.adesc[v] = None
    for k in data.rset:
        if data.L != k and data.rdesc[k] == x:
            data.rdesc[k] = None

#This function save's all the registers to memory at the end of a basic block
def save_to_memory() :
    for k in data.rset :
        push(k)
    
