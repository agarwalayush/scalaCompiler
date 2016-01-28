import classes
import il_parser
import itertools
import register_allocator

def addStimulator(obj):
    return ["mov eax, "+ obj.in1,"add eax, "+ obj.in2,"mov [{}], eax".format(obj.out)]

def subStimulator(obj):
    return ["mov eax, "+ obj.in1,"sub eax, "+ obj.in2,"mov [{}], eax".format(obj.out)]

def multStimulator(obj):
    return ["mov eax, "+ obj.in1,"imul eax, "+obj.in2,"mov [{}], eax".format(obj.out)]

def divStimulator(obj):
    return ["mov eax, "+ obj.in1, "mov edx, 0", "mov ebx, "+ obj.in2 ,"idiv ebx","mov [{}], eax\n".format(obj.out)]

def assemblyGenerator(ins_list, v_set, r_set):
    assembly = []
    functionMap = {'+': addStimulator, '-': subStimulator, '*': multStimulator, '/': divStimulator}
    for i in ins_list:
        (x, y, z, inno) = (i.out, i.in1, i.in2, i.no)
        (reg1, reg2, reg3) = allocator(x, y, z, inno, v_set, r_set)
        assembly+= functionMap[i.type](i)
    print('\n'.join(assembly))

if __name__ == "__main__" :
    (ins_list, var_set) = parse_file('instr.il')
    r_set = {}
    v_set = {}
    r_name = ["eax", "ebx", "ecx", "edx"]
    #initialize rSet
    initReg(r_set, r_name)
    initVar(v_set, var_set)
    buildTable(ins_list, v_set)
    assemblyGenerator(ins_list, r_set)

