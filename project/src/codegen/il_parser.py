#!/usr/bin/env python

import sys
import data
from data import debug
def check_variable(var_bar) :
    try :
        int(var_bar)
        return False
    except:
        return True

def check_branching(type) :
    return type in ['jump', 'call', 'goto', 'label','printstr', 'jle', 'jg', 'je', 'jge', 'jl', 'jne']

def check_array(type) :
    return type in ['array', '<-', '->']

def parse_il(file_object) :
    flag = 0
    argcount = 8
    localcount = -4
    scope_func = 0
    for line in file_object.readlines():
        if ',' not in line : continue
        list_temp = line.split(',')
        list_i = [None]*5
        list_i[:len(list_temp)] = list_temp
        list_i[len(list_temp)-1] = list_i[len(list_temp)-1].replace('\n', '')
        if not check_branching(list_i[1]) and not check_array(list_i[1]):
            for i in range(2,len(list_temp)) :
                if check_variable(list_i[i]) :
                    if(flag == 1):
                        if(list_i[i] not in data.memmap[scope_func].keys()):
                            if(i > 0 and list_i[1] == 'arg'):
                                data.memmap[scope_func][list_i[i]] = str(argcount) + "(%ebp)"
                                argcount += 4
                            elif(list_i[i] not in data.globmap):
                                data.memmap[scope_func][list_i[i]] = str(localcount) + "(%ebp)"
                                localcount -= 4
                    else:
                        data.globmap.add(list_i[i])
                    data.vset.add(list_i[i])
        if list_i[1] == 'label' and list_i[2].startswith('func'):
            flag = 1
            scope_func = list_i[2]
            data.memmap[scope_func] = {}
        if(list_i[1] == 'ret'):
            flag = 0
            data.num_var[scope_func] = -localcount
        if list_i[1] == 'array':
            data.arrayset[list_i[2]] = list_i[3]
        if list_i[1] == 'printstr' :
            data.stringMap['str'+list_i[0]] = list_i[2]
        debug(list_i[0])
        if list_i[1] == "cmp" :
            data.raw.append(data.instruction3ac(int(list_i[0]),list_i[1],list_i[2],list_i[3],None))
            continue
        data.raw.append(data.instruction3ac(int(list_i[0]),list_i[1],list_i[3],list_i[4],list_i[2]))


def parse_il_from_list(lst) :
    index = 0
    for line in lst :
        index+=1
        if ',' not in line :
            continue
        list_temp = line.split(',')
        list_i = [1]+[None]*4
        list_i[1:len(list_temp)+1] = list_temp
        list_i[len(list_temp)-1] = list_i[len(list_temp)-1].replace('\n', '')
        if not check_branching(list_i[1]) and not check_array(list_i[1]):
                for i in range(2,len(list_temp)) :
                    if check_variable(list_i[i]) :
                        data.vset.add(list_i[i])
                if list_i[1] == 'array':
                            data.arrayset[list_i[2]] = list_i[3]
                if list_i[1] == 'printstr' :
                    data.stringMap['str'+list_i[0]] = list_i[2]
                debug(list_i[0])
                if list_i[1] == "cmp" :
                    data.raw.append(data.instruction3ac(int(list_i[0]),list_i[1],list_i[2],list_i[3],None))
                continue
        data.raw.append(data.instruction3ac(int(list_i[0]),list_i[1],list_i[3],list_i[4],list_i[2]))
