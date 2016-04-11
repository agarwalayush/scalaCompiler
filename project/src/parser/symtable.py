
class Scope:

    id = 1
    def __init__(self, parent = None, name = "Main"):
        self.name = name
        self.id = Scope.id
        Scope.id = Scope.id + 1
        self.parent = parent
        self.child_list = []
        if(parent != None):
            parent.child_list.append(self)
        self.symbol_list = {}
        #Todo: currently the function_list is a dictionary of function names and their number of arguments, update in type checking
        self.function_list = {}
        self.object_list = []
        self.code = []
        self.offset = 0
        self.total_width = 0
        self.num_arg = 0

    def add_symb(self, symbolname, attr_dict):
            self.symbol_list[symbolname] = attr_dict

    def add_func(self, funcname, attr_dict):
            self.function_list[funcname] = attr_dict

    def check_for_variable_declaration(self, var):
        flag = 0
        c_scope = self
        while(c_scope != None):
            if(var in c_scope.symbol_list.keys()):
                flag = 1
                break
            c_scope = c_scope.parent
        return (flag, c_scope)


    def check_for_function_declaration(self, var):
            flag = 0
            c_scope = self
            while(c_scope is not None):
                if(var in c_scope.function_list.keys()):
                    flag = 1
                    break
                c_scope = c_scope.parent
            return (flag, c_scope)






