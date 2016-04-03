
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

    def check_for_the_variable_declaration(self, var):
        flag = 0
        c_scope = self
        while(c_scope != None):
            if(var in c_scope.symbol_list.keys()):
                flag = 1
                break
            c_scope = self.parent
        return flag

    def check_for_the_function_declaration(self, var):
            flag = 0
            c_scope = self
            while(c_scope != None):
                if(var in c_scope.function_list.keys()):
                    flag = 1
                    break
                c_scope = self.parent
            return flag





