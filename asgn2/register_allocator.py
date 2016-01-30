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

def STORE(store_list):
    var_push = reg_y.n_var
    var_push.Reg.remove(reg_y)
    var_push.inmem = True
    return []

def LOAD(reg, var) :
    v_set[var].Reg.append(reg)
    return []

class RegisterAllocator :
    def __init__(self, instruction_list) :
        #do something
        pass
    
    def allocator(x, y, z = None, inno = 0, v_set = None , r_set = None):
        def inallocator(var_name, flag): #flag true if z != x
            '''Returns (reg_name, load, store)'''
            if len(v_set[var_name].Reg) != 0:
                temp = v_set[var_name].Reg[0]
                v_set[var_name].Reg.clear()
                return (temp, 0, 0)

            for reg in r_set.keys() :
                if r_set[reg].free == True:
                    return (reg, 1, 0)

            min_reg = None
            nxtuse = -1
            for reg in r_set.keys() :
                var = r_set[reg].n_var
                if len(v_set[var].Reg) > 1 or  v_set[var].inmem == True or (var == x and flag == True) or v_set[var].dead[inno] == True :
                    return (reg, 1, 0)
                if(nxtuse < v_set[var].nextuse[inno]):
                    nxtuse = v_set[var].nextuse[inno]
                    min_reg = reg
                return (min_reg, 1, 1)

        def outallocater(var_name):
            '''Returns (reg_name, store)'''
            if len(v_set[var_name].Reg) != 0:
                temp = v_set[var_name].Reg[0]
                v_set[var_name].Reg.clear()
                return (temp, 0)

            for reg in r_set.keys() :
                if r_set[reg].free == True:
                    return (reg, 0)

            min_reg = None
            nxtuse = -1
            for reg in r_set.keys() :
                var = r_set[reg].n_var
                if len(v_set[var].Reg) > 1 or  v_set[var].inmem == True or var == y or var == z or v_set[var].dead[inno] == True :
                    return (reg, 0)
                if(nxtuse < v_set[var].nextuse[inno]):
                    nxtuse = v_set[var].nextuse[inno]
                    min_reg = reg
                return (min_reg, 1)

        ret_list = []
        (reg_y, load, store) = inallocater(y, z != x)

        if store :
            ret_list.append(STORE(reg_y))

        if load :
            ret_list.append(LOAD(reg_y, y))

        (reg_z, load, store) = inallocater(z, y != x)

        if store :
            ret_list.append(STORE(reg_z))

        if load :
            ret_list.append(LOAD(reg_z, z))

        (reg_x, store) = outallocater(x)
        ret_list.append(functionMap[operator]())
        v_set[x].append(reg_x)
        v_set[x].inmem = False 
        return x
