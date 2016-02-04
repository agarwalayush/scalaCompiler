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
    return type in ['jump', 'call', 'goto', 'label', 'goto']

def parse_il(file_object) :
        for line in file_object.readlines():
            if ',' not in line : continue
            list_temp = line.split(',')
            list_i = [None]*5
            list_i[:len(list_temp)] = list_temp
            list_i[len(list_temp)-1] = list_i[len(list_temp)-1].replace('\n', '')
            if not check_branching(list_i[1]):
                for i in range(2,len(list_temp)) :
                    if check_variable(list_i[i]) :
                        data.vset.add(list_i[i])
            debug(list_i[0])
            data.raw.append(data.instruction3ac(int(list_i[0]),list_i[1],list_i[3],list_i[4],list_i[2]))
