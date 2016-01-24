class instruction3ac :
    def __init__(self,type, in1, in2, out) :
        self.type, self.in1, self.in2, self.out = type, in1, in2, out

def parse_file(file_name) :
    ret_val = []
    with open(file_name,"r") as file :
        for line in file.readline():
            i, operator,out , op1, op2 = line.split(',')
            ret_val.append(instruction3ac(operator, op1, op2, out))
    return ret_val
