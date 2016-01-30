#!/usr/bin/env python

import sys
import classes
def check_variable(var_bar) :
    try :
        int(var_bar)
        return False
    except:
        return True

def parse_il(file_name) :
    ret_val = []
    vset = {}
    with open(file_name,"r") as file :
        for line in file.readlines():
            list_temp = line.split(',')
            list_i = [None]*5
            list_i[:len(list_temp)] = list_temp
            list_i[len(list_temp)-1] = list_i[len(list_temp)-1].replace('\n', '')
            for i in range(2,len(list_temp)) :
                if check_variable(list_i[i]) :
                    vset[list_i[i]] = Variable()
            ret_val.append(instruction3ac(list_i[0],list_i[1],list_i[3],list_i[4],list_i[2]))
    return (ret_val,vset)

