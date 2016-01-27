import instruction3ac
import il_parser

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

