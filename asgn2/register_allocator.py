import classes

#This file contains routines for getting Z', Y' and L subject to the conditions imposed by the operators


# This function pushes the variable stored at "reg" into memory and frees it 
def push(register):
    out.add("mov [{}], {}".format(rdesc[register], register))
    adesc[rdesc[register]] = None
    rdesc[register] = None

#This function takes a variable var and assigns zprime
def getz(var):
    if adesc[var] != None:
        zprime = adesc[var]
    else:
        zprime = var

#This function takes variables x, y and the current instruction number returns a suitable memory location / register L
#special: register is given when a particular register is needed, like eax for division
#flag: 1 if there is a constraint on atmost 1 on zprime and L to be a memory location, else 0

def getreg(y, ino, flag = 0, special = None):
    if special != None :
        L = None
    elif adesc[y] != None and symtable[ino][y] == INF:
        L = adesc[y]
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
