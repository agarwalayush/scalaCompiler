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
            list_temp = line.split(',')
            list_i = [None]*5
            list_i[:len(list_temp)] = list_temp
            list_i[len(list_temp)-1] = list_i[len(list_temp)-1].replace('\n', '')
            for i in range(2,len(list_temp)) :
                if check_variable(list_i[i]) :
                    vset.add(list_i[i])
            ret_val.append(instruction3ac(list_i[1],list_i[3],list_i[4],list_i[2]))
    return (ret_val,vset)

class instruction3ac :
    def __init__(self,type, in1, in2, out) :
        self.type, self.in1, self.in2, self.out = type, in1, in2, out


def addStimulator(obj):
    return ["mov eax, "+ obj.in1,"add eax, "+ obj.in2,"mov [{}], eax".format(obj.out)]

def subStimulator(obj):
    return ["mov eax, "+ obj.in1,"sub eax, "+ obj.in2,"mov [{}], eax".format(obj.out)]

def multStimulator(obj):
    return ["mov eax, "+ obj.in1,"imul eax, "+obj.in2,"mov [{}], eax".format(obj.out)]

def divStimulator(obj):
    return ["mov eax, "+ obj.in1, "mov edx, 0", "mov ebx, "+ obj.in2 ,"idiv ebx","mov [{}], eax\n".format(obj.out)]

def assemblyGenerator(ins_list):
    assembly = []
    functionMap = {'+': addStimulator, '-': subStimulator, '*': multStimulator, '/': divStimulator}
    for i in ins_list:
            assembly+= functionMap[i.type](i)
    print('\n'.join(assembly))

if __name__ == "__main__" :
    (ins_list, var_list) = parse_file('instr.il')
    assemblyGenerator(ins_list)


