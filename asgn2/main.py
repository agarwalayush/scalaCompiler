#/usr/bin/env python
import data
from il_parser import *
import register_allocator
import assembly_generator
import sys

'''def addStimulator(obj):
    return ["mov eax, "+ obj.in1,"add eax, "+ obj.in2,"mov [{}], eax".format(obj.out)]

def subStimulator(obj):
    return ["mov eax, "+ obj.in1,"sub eax, "+ obj.in2,"mov [{}], eax".format(obj.out)]

def multStimulator(obj):
    return ["mov eax, "+ obj.in1,"imul eax, "+obj.in2,"mov [{}], eax".format(obj.out)]

def divStimulator(obj):
    return ["mov eax, "+ obj.in1, "mov edx, 0", "mov ebx, "+ obj.in2 ,"idiv ebx","mov [{}], eax\n".format(obj.out)]
'''

def assemblyGenerator(operator, ):
    assembly = []
    functionMap = {'+': addStimulator, '-': subStimulator, '*': multStimulator, '/': divStimulator}
    for i in ins_list:
        (x, y, z, inno) = (i.out, i.in1, i.in2, i.no)
        (reg1, reg2, reg3) = allocator(x, y, z, inno, v_set, r_set)
        assembly+= functionMap[i.type](i)
    print('\n'.join(assembly))

if __name__ == "__main__" :
    parse_il(sys.argv[1])
    assembly_generator.assembly_generator()
