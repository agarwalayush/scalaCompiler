
class Scope:

    id = 1

    def __init__(self, parent = None):
        self.id = Scope.id
        Scope.id = Scope.id + 1
        self.parent = parent
        self.child_list = []
        if(parent != None):
            parent.child_list.append(self)
        self.symbol_list = {}
        self.function_list = {}
        self.code = []
        self.offset = 0
        self.total_width = 0

    def add_symb(self, symbolname, attr_dict):
            self.symbol_list[symbolname] = attr_dict

    def add_func(self, funcname, attr_dict):
            self.function_list[funcname] = attr_dict

    
