#!/usr/bin/env python

import sys

def check_variable(var_bar) :
    try :
        int(var_bar)
        return False
    except:
        return True

def parse_file(file_name) :
    ret_val = []
    vset = set()
    with open(file_name,"r") as file :
        for line in file.readlines():
            list_i = line.split(',')
            list_i[4] = (list_i[4])
            for i in range(2,4) :
                if check_variable(list_i[i]) :
                    vset.add(list_i[i])
            ret_val.append(instruction3ac(list_i[1],list_i[3],list_i[4],list_i[2]))
    return (ret_val,vset)

class instruction3ac :
    def __init__(self,type, in1, in2, out) :
        self.type, self.in1, self.in2, self.out = type, in1, in2, out

if __name__ == "__main__" :
    parse_file('instr.il')
