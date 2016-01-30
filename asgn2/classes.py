import sys

class instruction3ac :
    def __init__(self, no, type, in1, in2, out) :
        self.no, self.type, self.in1, self.in2, self.out = no, type, in1, in2, out

class Register :
    def __init__(self) :
         n_var
         free = True


class Variable :
    def __init__(self) :
        self.Reg = []
        self.inmem = False
        self.dead = {}
        self.nextuse = {}
