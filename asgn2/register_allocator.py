import data
import math

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
def transform(str):
    if str in data.rset :
        return str
    else:
        return "[" + str + "]"

#This function initializes some global variables

def ini():
    data.L = None
    data.yprime = None
    data.zprime = None



# This function pushes the variable stored at "reg" into memory and frees it 
def push(register):
    data.out.add("mov [{}], {}".format(data.rdesc[register], register))
    data.adesc[rdesc[register]] = None
    data.rdesc[register] = None

#This function takes a variable var and assigns zprime
def getz(var):
    if data.adesc[var] != None:
        data.zprime = data.adesc[var]
    else:
        data.zprime = var

#This function takes variables x, y and the current instruction number returns a suitable memory location / register L
#special: register is given when a particular register is needed, like eax for division
#flag: 1 if there is a constraint on atmost 1 on zprime and L to be a memory location, else 0

def getreg(x, y, ino, flag = 0, special = None):
    if special != None :
        L = special
    elif adesc[y] != None and symtable[ino][y] == INF:
        L = adesc[y]
    elif adesc[x] != None:
        L = adesc[x]
    if L == None:
        for k in rset.keys():
            if rdesc[k] == None:
                L = k
    if L == None :
        if(symtable[ino][x] != INF or (flag == 1 and zprime not in rset)):
           nxtuse = -1
           for k in rset.keys():
               if nxtuse < symtable[ino][rdesc[k]]:
                   L = rdesc[k]
                   nxtuse = symtable[ino][rdesc[k]]
        else:
            L = x
    if L in rset and rdesc[L] != None:
        push(L)

#This function gives Y' and moves Y' to L if value of Y in not already in L
def gety(var):
    if rdesc[var] != None:
        yprime = rdesc[var]
    else:
        yprime = var
    if yprime != L :
        out.add("mov " + transform(L) + ", " + transform(yprime))

#This function frees a register if the variable it stores becomes dead
#TODO: handle the global variable
def freereg(var, ino):
    if symtable[ino][var] == INF and adesc[var] != None:
        rdesc[adesc[var]] = None
        adesc[var] = None

#This function updates the address descriptor corresdonding to the out variable
def update(var):
    if L in rset:
        adesc[var] = L
    else:
        adesc[var] = None
    for k in rset:
        if L != k and rdesc[k] == x:
            rdesc[k] = None
