import classes

def buildTable(ins_list, v_set):
    '''scan from backwards to set the live ranges
    assuming all variables to be dead on exit'''
    for ins in reversed(ins_list):
        (inno, x, y, z) = (ins.out, ins.in1, ins.in2)
        if inno == 1 : break
        for k in v_set.keys():
            if k == x :
                v_set[k].dead[inno - 1] = True
            elif k == y or k == z :
                v_set[k].dead[inno - 1] = False
                v_set[k].nextuse[inno - 1] = inno
            else:
                if inno == len(ins_list):
                    v_set[k].dead[inno] = True
                else:
                    v_set[k].dead[inno - 1] = v_set.dead[inno]
                    v_set[k].nextuse[inno - 1] = v_set.nextuse[inno]

def initReg(rset, rname) :
    for x in rname:
        rset[x] = Register()

def initVar(vset, v_name) :
    for x in v_name:
        vset[x] = Variable()

class RegisterAllocator :
    def __init__(self, instruction_list) :
        #do something
        pass
    
    def get_reg(variable) :
        return ('eax', False)

    def allocator(x, y, z = None, inno, v_set = None , r_set = None):
        def inallocator(var_name, flag): #flag true if z != x
            if len(v_set[var_name].Reg) != 0:
                return v_set[var_name].Reg[0]
            for reg in r_set.keys() :
                if r_set[reg].free == True:
                    return reg
            min_reg = None
            nxtuse = -1
            for reg in r_set.keys() :
                var = r_set[reg].n_var
                if len(v_set[var].Reg) > 1 or  v_set[var].inmem = True or var == x and flag = True or v_set[var].dead[inno] = True:
                    return reg
                if(nxtuse < v_set[var].nextuse[inno]):
                    nxtuse = v_set[var].nextuse[inno]
                    min_reg = reg
                return min_reg    
        return x
