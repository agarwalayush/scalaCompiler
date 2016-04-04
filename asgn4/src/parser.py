import ply.yacc as yacc
import sys
import logging
from lexer import tokens
import os
import re
from symtable import *

CURR = Scope()
ROOT = CURR
CLASS_SCOPE = []
OBJECT_SCOPE = []

temp_count = 0
label_count = 0
def newtmp(dataType= 'Unit'):
    global temp_count
    global CURR
    symbolname= "temp" + str(temp_count)
    temp_count += 1
    attr= {'Type' : dataType}
    CURR.add_symb(symbolname, attr)
    return symbolname

def newlabel():
    global label_count
    labelname= "label" + str(label_count)
    label_count += 1
    return labelname

def higher(type1,type2):
    if((type1,type2) == ('Int', 'Float')):
        return type2
    elif ((type1,type2) == ( 'Float','Int')):
        return type1
    else:
        return type1

class Node(object):
    id = 1
    def __init__(self, name, child_list, type = "Unit", size = None, val = None, code = [], place = None):
        self.name = name
        self.child_list = child_list
        self.id = Node.id
        Node.id += 1
        self.type = type
        self.val = val
        self.code = code
        self.place = place
        self.size = size

def transform(k):
    list = k.split(".")
    return list.join("_")

def create_leaf(name1,name2,dataType="Unit"):
    leaf1 = Node(name2,[],dataType)
    leaf2 = Node(name1,[leaf1],dataType)
    return leaf2



#####################################

def p_compilation_unit(p):
    'compilation_unit :  import_declarations_extras classes_objects_list'
    p[0] = Node("compilation_unit",[p[1],p[2]], None, None, None, p[2].code)


    print(('\n').join(p[0].code))


def p_import_declarations_extras(p):
    '''import_declarations_extras : import_declarations
                                          | empty'''
    p[0] = Node("import_declarations_extras", [p[1]])

def p_import_declarations(p):
    '''import_declarations :  import_declaration
                                    | import_declarations import_declaration'''
    if len(p) == 2 :
        p[0] = Node("import_declarations",[p[1]])
    else :
        p[0] = Node("import_declarations",[p[1],p[2]])


def p_import_declaration(p):
    '''import_declaration :  K_IMPORT ambiguous_name'''
    child = create_leaf("K_IMPORT", p[1])
    p[0] = Node("import_declaration",[child, p[2]])

def p_classes_objects_list(p):
    '''classes_objects_list : classes_objects_list  class_and_objects_declaration
                              | class_and_objects_declaration '''
    if len(p) == 3 :
        p[0] = Node("classes_objects_list",[p[1],p[2]], None, None, None, p[1].code + p[2].code )
    else :
        p[0] = Node("classes_objects_list",[p[1]], None, None, None, p[1].code)
        

def p_class_and_objects_declaration(p):
    '''class_and_objects_declaration : object_declaration
                                                | class_declaration'''

    p[0] = Node("class_and_objects_declaration",[p[1]], None, None, None, p[1].code)


def p_object_declaration(p):
    'object_declaration : ObjectDeclare block'
    p[0] = Node("class_object_declaration",[p[1], p[2]], None, None, None, p[2].code)
#    print(p[0].code)

def p_object_declare(p):
    '''ObjectDeclare : K_OBJECT IDENTIFIER super '''
    global CURR
    child1 = create_leaf("K_OBJECT", p[1])
    child2 = create_leaf("IDENTIFIER", p[2])
    CURR.object_list.append(p[2])
    p[0] = Node("ObjectDeclare",[child1, child2, p[1]])
    
def p_class_type(p):
    '''class_type : IDENTIFIER
                    | K_WITH class_type'''
    if len(p) == 2 :
        child1 = create_leaf("IDENTIFIER", p[1])
        p[0] = Node("class_type",[p[1]])
    else :
        child1 = create_leaf("K_WITH", p[1])
        p[0] = Node("class_type",[p[1],p[2]])


def p_super(p):
    '''super : K_EXTENDS class_type
              | empty'''
    if len(p) == 2 :
        p[0] = Node("class_type",[p[1]])
    else :
        child1 = create_leaf("K_EXTENDS", p[1])
        p[0] = Node("class_type",[p[1],p[2]])



def p_class_declaration(p):
    '''class_declaration : class_header class_body'''
    p[0] = Node("class_type",[p[1],p[2]],None, None, None, p[2].code)


def p_class_header(p):              # classes can't be defined inside objects
    '''class_header : K_CLASS IDENTIFIER class_begin_bracket argument_header RPAREN super'''
    global CURR
    child1 = create_leaf("K_CLASS", p[1])
    child2 = create_leaf('IDENTIFIER',p[2])
    child3 = create_leaf('RPAREN', p[4])
    CURR.name = p[2]
    p[0] = Node("class_header",[child1,child2,p[3],p[4],child3,p[5]])


def p_class_begin_bracket(p):
    '''class_begin_bracket : LPAREN'''
    global CURR
    global CLASS_SCOPE
    NEW_ENV = Scope(CURR)
    CURR = NEW_ENV
    CLASS_SCOPE.append(CURR)
    child = Node('LPAREN',p[1])
    p[0] = Node('class_begin_bracket',[child])

def p_class_body(p):
    '''class_body : BLOCK_BEGIN class_body_declarations_extras block_end '''
    child = create_leaf('BLOCK_BEGIN',p[1])
    p[0] = Node('class_body', [child,p[2],p[3]], None, None, None, p[1].code)

def p_block_end(p):
    '''block_end : BLOCK_END'''
    global CURR
    PREV_ENV = CURR.parent
    CURR=PREV_ENV
    child = create_leaf('BLOCK_END',p[1])
    p[0]= Node('block_end',[child])


def p_class_body_declarations_extras(p):
    '''class_body_declarations_extras : class_body_declarations
                                                    | empty'''
    p[0] = Node('class_body_declarations_extras' , [p[1]], None, None, None, p[1].code)

def p_class_body_declarations(p):
    '''class_body_declarations : class_body_declaration
                                          | class_body_declarations class_body_declaration'''
    if(len(p)==2):
        p[0] = Node('class_body_declarations', [p[1]], None, None, None, p[1].code)
    else:
        p[0] = Node('class_body_declarations' , [p[1],p[2]], None, None, None, p[1].code + p[2].code)


def p_class_body_declaration(p):
    '''class_body_declaration : local_variable
                                          | method_declaration'''
    p[0] = Node('class_body_declaration' , [p[1]])
    p[0] = Node('class_body_declaration' , [p[1]], None, None, None, p[1].code)



#p[1].val currently contains the number of arguments
def p_argument_header(p):
    '''argument_header : argument_list
                        | empty '''
    global CURR
    if(p[1].val is None): p[1].val = 0
    if(p[1].place is None): p[1].place = []
    p[0]= Node("argument_header", [p[1]], None, None, val = p[1].val, place = p[1].place)
    if(~(p[1].val is None)):
        CURR.num_arg = p[1].val

def p_arguement_list(p):
    '''argument_list : argument
                        | argument_list COMMA argument'''

    if (len(p) == 2):
        p[0] = Node("argument_list", [p[1]],[p[1].type],[p[1].size], val = 1, place = p[1].place)
    else:
        child = create_leaf("COMMA", p[2])
        p[0] = Node("argument_list", [p[1], child, p[3]], p[3].type.append(p[1].type), p[3].size + p[1].size, val = p[1].val + 1, place = p[1].place + p[3].place)
        
#checking the identifiers !!
def p_argument(p):
    '''argument : IDENTIFIER COLON type'''
    global CURR
    child1 = create_leaf("IDENTIFIER", p[1])
    child2 = create_leaf("COLON", p[2])
    attr = {}
    attr['Type']=p[3].type
    attr['Size']=p[3].size
    CURR.add_symb(p[1],attr)
    p[0] = Node("argument", [child1, child2, p[3]],p[3].type,p[3].size, place = [])



def p_semi(p):
    '''semi : SEMI_COLON
              | NEWLINE'''
    child =create_leaf('SEMI', p[1])
    p[0] = Node("semi",[child])


def p_method_declaration(p):
    '''method_declaration : method_header method_body '''
    p[0]= Node('method_declaration',[p[1], p[2]], None, None, None, p[1].code + p[2].code)

#adding label of the function by refrecing the class/obejct calling it and adding the number of arguments in the scope of the enclosing class

def p_method_header(p):
    '''method_header :  K_DEF IDENTIFIER func_begin_bracket argument_header RPAREN COLON method_return_type ASSIGN
                        | K_DEF IDENTIFIER func_begin_bracket argument_header RPAREN ASSIGN
                        | K_DEF IDENTIFIER func_begin_bracket argument_header RPAREN'''
    global CURR
    child1= create_leaf('K_DEF',p[1])
    child2 = create_leaf('IDENTIFIER',p[2])
    child3 = create_leaf('RPAREN', p[5])
    attr = {}
    func_label = str(CURR.parent.id) + "_" + p[2]
    l1 = ["label," + func_label]
    attr['Type'] = p[4].type
    print(p[4].val)
    attr['num_arg'] = p[4].val
    if(len(p)==6):
        attr['ReturnType'] = 'Unit'
        p[0]=Node('method_header',[child1,child2,p[3],p[4],p[5]], None, None, None, l1)
    elif(len(p)==7):
        attr['ReturnType'] = 'Unit'
        child4= create_leaf('ASSIGN',p[6])            
        p[0]=Node('method_header',[child1,child2,p[3],p[4],p[5],child4], None, None, None, l1)
    else:
        print(len(p))
        attr['ReturnType'] = p[7].type
        child4 = create_leaf('COLON',p[6])
        child5= create_leaf('ASSIGN',p[8])            
        p[0]=Node('method_header',[child1,child2,p[3],p[4],p[5],child4,p[7],child5], None, None, None, l1)
    print(CURR.parent.id)
    CURR.parent.function_list[p[2]] = attr
        # def p_method_return_type_extras(p):
        #     '''method_return_type_extras : COLON method_return_type ASSIGN method_body
        #                                           | ASSIGN method_body
        #                                           | empty method_body'''

def p_method_return_type(p):
    '''method_return_type : type'''
    p[0]= Node('method_return_type',[p[1]], p[1].type, p[1].size)


def p_func_begin_bracket(p):
    '''func_begin_bracket : LPAREN'''
    global CURR
    NEW_ENV = Scope(CURR)
    CURR = NEW_ENV
    child = Node('LPAREN',p[1])
    p[0] = Node('func_begin_bracket',[child])



def p_method_body(p):
    '''method_body : BLOCK_BEGIN block_body block_end'''
    child=create_leaf('BLOCK_BEGIN', p[1])
    p[0] = Node('method_body', [child,p[2],p[3]], None, None, None, p[2].code)


################################################

#checking whether the identifiers are referenced by their correct names in expressions and checking whether they
#are present in any of their parent scopes
# locals and globals having the same name
def p_expression(p):
    '''expression : or_expression'''
    p[0] = Node("expression", [p[1]], p[1].type, None, None, p[1].code, p[1].place)


def p_or_expression(p):
    '''or_expression : and_expression
                            | or_expression OR and_expression'''
    if(len(p) == 2):
        p[0] = Node("or_expression", [p[1]], p[1].type, None, None, p[1].code, p[1].place)
    else:
        child = create_leaf("OR", p[2])
        temp = newtmp()
        l1 = ["|," + temp + "," + p[1].place + "," + p[3].place]
        p[0] = Node("or_expression", [p[1], child, p[2]], p[3].type, None, None, p[1].code + p[3].code + l1, temp)

def p_and_expression(p):
    '''and_expression : xor_expression
                        | and_expression AND xor_expression'''
    if(len(p) == 2):
        p[0] = Node("and_expression", [p[1]], p[1].type, None, None, p[1].code, p[1].place)
    else:
        child = create_leaf("AND", p[2])
        temp = newtmp()
        l1 = ["&," + temp + "," + p[1].place + "," + p[3].place]
        p[0] = Node("and_expression", [p[1], child, p[2]], p[3].type, None, None, p[1].code + p[3].code + l1, temp)

def p_xor_expression(p):
    '''xor_expression : equality_expression
                            | xor_expression XOR equality_expression'''
    if(len(p) == 2):
        p[0] = Node("xor_expression", [p[1]], p[1].type, None, None, p[1].code, p[1].place)
    else:
        child = create_leaf("XOR", p[2])
        temp = newtmp()
        l1 = ["^," + temp + "," + p[1].place + "," + p[3].place]
        p[0] = Node("xor_expression", [p[1], child, p[2]], p[3].type, None, None, p[1].code + p[3].code + l1, temp)

def p_equality_expression(p):
    '''equality_expression : relational_expression
                                    | equality_expression EQUAL relational_expression
                                    | equality_expression NEQUAL relational_expression'''
    if(len(p) == 2):
        p[0] = Node("equality_expression", [p[1]], p[1].type, None, None, p[1].code, p[1].place)
    elif p[2] == "==":
        child = create_leaf("EQUAL", p[2])
        temp1 = newtmp()
        temp2 = newtmp()
        l1 = ["^," + temp1 + "," + p[1].place + "," + p[3].place]
        l2 = ["-," + temp2 + ", 1, " + temp1]
        p[0] = Node("equality_expression", [p[1], child, p[3]], 'Bool', None, None, p[1].code + p[3].code + l1 + l2, temp2)
    elif p[2] == "!=":
        child = create_leaf("NEQUAL", p[2])
        temp = newtmp()
        l1 = ["^," + temp + "," + p[1].place + "," + p[3].place]
        p[0] = Node("equality_expression", [p[1], child, p[3]], 'Bool', None, None, p[1].code + p[3].code + l1, temp)

def p_relational_expression(p):
    '''relational_expression : add_expression
                                        | relational_expression GREATER_THAN add_expression
                                        | relational_expression GREATER_THAN_EQUAL add_expression
                                        | relational_expression LESS_THAN add_expression
                                        | relational_expression LESS_THAN_EQUAL add_expression'''
    if(len(p) == 2):
        p[0] = Node("relational_expression", [p[1]], p[1].type, None, None, p[1].code, p[1].place)
        return
    child = create_leaf("RelOp", p[2])
    if(p[2] == ">"):
        rel = jg
    elif p[2] == ">=":
        rel = jge
    elif p[2] == "<":
        rel = jl
    elif p[2] == "<=":
        rel = jle
        temp = newtmp()
        etrue = newlabel()
        efalse = newlabel()
        l1 = ["cmp, " + p[1].place + ", " + p[3].place]
        l2 = [rel + "," + etrue]
        l3 = ["=," + temp + ", 0"]
        l4 = ["goto, " + efalse]
        l5 = ["label, " + etrue]
        l6 = ["=," + temp + ", 1"]
        l7 = ["label, " + efalse]
        p[0] = Node("relational_expression", [p[1], child, p[3]], 'Bool', None, None, p[1].code + p[3].code + l1 + l2 + l3, l4 + l5 + l6 + l7, temp)

def p_add_expression(p):
    '''add_expression : mult_expression
                                    | add_expression PLUS mult_expression
                                    | add_expression MINUS mult_expression'''
    if(len(p)==2):
        p[0] = Node("add_expression", [p[1]], p[1].type, None, None, p[1].code, p[1].place)

    else:
        child = create_leaf("PLUS_MINUS", p[2])
        temp = newtmp()
        l1 = p[2] + ", " + temp + ", " + p[1].place + "," + p[3].place
        p[0] = Node("add_expression", [p[1], child, p[3]], higher(p[1].type,p[3].type), None, None, p[1].code + p[3].code + l1, temp)

def p_mult_expression(p):
    '''mult_expression : unary_expression
                         | mult_expression DIVIDE unary_expression
                         | mult_expression MULT unary_expression
                         | mult_expression MOD unary_expression'''
    if(len(p) == 2):
        p[0] = Node("mult_expression", [p[1]], p[1].type, None, None, p[1].code, p[1].place)
    else :
        child = create_leaf("DIV_MOD", p[2])
        temp = newtmp()
        l1 = [p[2] + ", " + temp + ", " + p[1].place + "," + p[3].place]
        p[0] = Node("mult_expression", [p[1], child, p[3]], None, None, None, p[1].code + p[3].code + l1, temp)


def p_unary_expression(p):
    '''unary_expression : PLUS unary_expression
                                 | MINUS unary_expression
                                 | postfix_not_expression'''
    if(len(p) !=2):
        child = create_leaf("PLUS_MINUS", p[1])
        if(p[1] == MINUS):
            l1 = ["-, " + p[2].place + ", 0, " + p[2].place]
            p[0] = Node("unary_expression", [child, p[2]], p[2].type, None, None, p[2].code + l1, p[2].place)
        else:
            p[0] = Node("unary_expression", [child, p[2]], p[2].type, None, None, p[2].code, p[2].place)
    else:
        p[0] = Node("unary_expression", [p[1]], p[1].type, None, None, p[1].code, p[1].place)

def p_postfix_not_expression(p):
    '''postfix_not_expression : postfix_expression
    | NOT unary_expression'''
    global CURR
    if(len(p) != 2):
        child = create_leaf("NOT", p[1])
        l1 = ["!, " + p[2].place + "," + p[2].place]
        p[0] = Node("postfix_not_expression", [child, p[2]], p[2].type, None, None, p[2].code + l1, p[2].place)
    else:
        p[0] = Node("postfix_not_expression", [p[1]], p[1].type, None, None, p[1].code, p[1].place)

def p_postfix_expression1(p):
    '''  postfix_expression : primary_no_new_array'''
    p[0] = Node("postfix_expression", [p[1]], p[1].type, None, None, p[1].code, p[1].place)

def p_postfix_expression2(p):
    #classes and objects not done
    '''  postfix_expression : ambiguous_name'''

    (x, y) = CURR.check_for_variable_declaration(p[1])
    if(x == 0):
        print('Undeclared variable')
        assert(false)
    else:
        holding_variable = str(y.id) + "_" + p[1]
        p[0] = Node("postfix_expression", [p[1]], p[1].type, None, None, p[1].code, holding_variable)


def p_primary_no_new_array(p):
    '''  primary_no_new_array : literal
                                | method_invocation
                                | LPAREN expression RPAREN
                                | array_invocation'''
    if(len(p) == 2):
        p[0] = Node("primary_no_new_array", [p[1]], p[1].type, None, None, p[1].code, p[1].place)
    else:
        child1 = create_leaf("LPAREN", p[1])
        child2 = create_leaf("RPAREN", p[3])
        p[0] = Node("primary_no_new_array", [child1, p[2], child2], p[2].type, None,None, p[2].code, p[2].place)

def p_literal(p):
    '''literal : STRING
            | CHAR
            | K_FALSE
            | K_TRUE
            | K_NULL
            | FLOAT
            | INT'''
    temp = newtmp()
    l1 = ["=, " + temp + ", " + str(p[1])]
    child = create_leaf("LITERAL", p[1])
    type = 'None'
    size = 0
    if (p[1] == 'STRING'):
        type = 'String'
    elif(p[1] == 'FALSE' or p[1] == 'TRUE'):
        type = 'Bool'
    elif (p[1] == 'CHAR'):
        type = 'Char'
        size =1
    elif (p[1] == 'INT'):
        type = 'Int'
        size = 2
    elif (p[1] == 'FLOAT'):
        type = 'Float'
        size = 4

    p[0] = Node("literal", [child], type, size, p[1], l1, temp)

def p_array_invocation(p):
    '''array_invocation : ambiguous_name SQUARE_BEGIN expression SQUARE_END '''
    global CURR
    temp = newtemp()
    l1 = ["<-" + temp + ", " + p[1].val + "," + p[3].place]
    type = CURR.symbol_list[p[1].value]['Type']
    #LOOKUP(ambiguous_name) in symbol_list
    if(~CURR.check_for_variable_declaration(p[1])):
        print('Undeclared variable')
        assert(false)
        child1 = create_leaf("SQUARE_BEGIN", p[2])
        child2 = create_leaf("SQUARE_END", p[4])
        p[0] = Node("array_invocation", [p[1], child1,p[3], child2], type, None, None, p[3].code + l1, temp)

def p_method_invocation(p):
    #TODO: classes and objects
    '''method_invocation : ambiguous_name LPAREN argument_list_extras RPAREN '''
    global CURR
    # check whether the function name is valid.
    (x, y) = CURR.check_for_function_declaration(p[1].val)
    if(x == 0):
        print("correct your semantics")
        assert(False)
    elif(p[3].val != y.function_list[p[1].val]["num_arg"]):
        print("wrong number of arguments!")
        assert(False)
    else:
        func_name = str(y.id) + "_" + p[1].val
    # implementing push in 3 address code


    child1 = create_leaf("LPAREN", p[2])
    child2 = create_leaf("RPAREN", p[4])
    code = []
    for k in p[3].place:
        code.append("pusharg, " + k)

    code.append("call," + func_name)
    p[0] = Node("method_invocation", [p[1], child1, p[3], child2], "Unit", None, None, p[1].code + p[3].code + code)




def p_argument_list_extras(p):
    '''argument_list_extras : argument_list
                                | empty'''
    if(p[1].val is None):
        p[1].val = 0

    if(p[1].place == None): p[1].place = []
    p[0] = Node("argument_list_extras", [p[1]], p[1].type, None, p[1].val, p[1].code, p[1].place)


def p_argument_list(p):
    '''argument_list : expression
                            | argument_list COMMA expression'''
    if(len(p) == 2):
        p[0] = Node("argumentList", [p[1]], [p[1].type], None, None, p[1].code, [p[1].place])
    else:
        child = create_leaf("COMMA", p[2]);
        p[0] = Node("argumentList", [p[1], child, p[3]], p[1].type + [p[3].type], None, None, p[1].code + p[3].code, p[1].place + [p[3].place])

def p_ambiguous_name(p):
    '''ambiguous_name : IDENTIFIER
                        | ambiguous_name DOT IDENTIFIER'''
    if(len(p)==2):
        child = create_leaf('IDENTIFIER', p[1])
        p[0] = Node('ambiguous_name', [child],None,None,p[1],[],None)
    else:
        #not implemented till now
        child = create_leaf('IDENTIFIER', p[3])
        child2 = create_leaf('.', p[2])
        p[0] = Node('ambiguous_name', [p[1],child2,child],None,None,p[1].value + '.' + p[3],[],None)



###################### BLOCK STATEMENTS


def p_block(p):
    '''block : block_begin block_body block_end '''
    p[0] = Node("block", [p[1], p[2], p[3]],code=p[2].code)
    #print(p[0].code)

def p_block_begin(p):
    '''block_begin : BLOCK_BEGIN'''
    global CURR
    NEW_ENV = Scope(CURR)
    CURR = NEW_ENV

    OBJECT_SCOPE.append(CURR)
    child = create_leaf("BLOCK_BEGIN", p[1])
    p[0] = Node("block_begin", [child])


def p_block_body(p):
    '''block_body : block_statement_list
                        | empty'''
    p[0] = Node("block_body", [p[1]], None, None, None, p[1].code)

def p_block_statement_list(p):
    '''block_statement_list : block_statement
                                    | block_statement_list block_statement'''
    if(len(p) == 2):
        p[0] = Node("block_statement_list", [p[1]], None, None, None, p[1].code)
    else:
        p[0] = Node("block_statement_list", [p[1], p[2]], None, None, None, p[1].code + p[2].code)


def p_block_statement(p):
    '''block_statement : local_variable
                        | method_declaration
                        | statement'''
    p[0] = Node('block_statement', [p[1]], None,None,None,p[1].code,None)

def p_variable_header(p):
    '''variable_header : K_VAL
                    | K_VAR '''
    child = create_leaf("K_VAL", p[1])
    p[0] = Node("variable_header", p[1])


def p_local_variable(p):
    'local_variable :   variable_header variable_body  semi'
    p[0] = Node("local_variable", [p[1], p[2],p[3]],None,None,None,p[2].code,None)


#### Checked , typed and scoped till here ############


def p_variable_body(p):
    #TODO: allow for instantiation of class objects and arrays
    '''variable_body : local_variable_and_type  ASSIGN  variable_rhs '''
    global CURR
    #only valid if RHS is variable_rhs = an expression
    code = ['=,' + p[1].place + ','+  p[3].place]
    child = create_leaf('ASSIGN', p[2])
    if( CURR.symbol_list[p[1].place]['Type'] == 'Undefined'):
    	CURR.symbol_list[p[1].place]['Type'] = p[3].type

    p[0] = Node('variable_body', [p[1],child,p[2]], None,None,None, p[3].code +code,None)

def p_type_of_variable(p):
    '''type_of_variable : IDENTIFIER COLON type'''
    global CURR
    if p[1] in CURR.symbol_list.keys():
        print("variable already defined")
        assert("False")
    else:
        attr = {}
        attr['Type'] = p[3].type
        attr['Size'] = p[3].size
        CURR.add_symb(p[1], attr)
        holding_variable = str(CURR.id) + "_" + p[1]
        print('....' , holding_variable)
        child1 = create_leaf("IDENTIFIER", p[1])
        child2 = create_leaf("COLON", p[2])
        p[0] = Node("type_of_variable", [child1, child2, p[3]],p[3].type,None,None,[], holding_variable)


def p_variable_rhs(p):
    '''variable_rhs : expression
                      | array_initializer
                      | class_instance_creation_expression '''
    p[0] = Node("variable_rhs", [p[1]], p[1].type, None,None, p[1].code, p[1].place)

def p_local_variable_and_type1(p):
	'''local_variable_and_type : type_of_variable'''
	p[0] = Node("local_variable_and_type", [p[1]], p[1].type, None, None, [], p[1].place)

def p_local_variable_and_type2(p):
    '''local_variable_and_type : IDENTIFIER'''
    global CURR
    if p[1] in CURR.symbol_list.keys():
        print("variable already defined")
        assert("False")
    else:
	    attr = {}
	    attr['Type'] = 'Undefined'
	    CURR.add_symb(p[1], attr)
	    child1 = create_leaf("IDENTIFIER", p[1])
	    p[0] = Node("local_variable_and_type", [child1], 'Undefined',None,None,None,p[1])

# def p_array_initializer(p):
# 	''' array_initializer : K_NEW K_ARRAY SQUARE_BEGIN type SQUARE_END LPAREN INT RPAREN
#                             | K_ARRAY LPAREN argument_list_extras RPAREN '''

def p_array_initializer(p):
    ''' array_initializer : K_NEW K_ARRAY SQUARE_BEGIN type SQUARE_END LPAREN INT RPAREN'''
    child1 = create_leaf('K_NEW', p[1])
    child2 = create_leaf('K_ARRAY', p[2])    
    child3 = create_leaf('SQUARE_BEGIN', p[3])
    child5 = create_leaf('SQUARE_END', p[5])
    child6 = create_leaf('LPAREN', p[6])
    child7 = create_leaf('INT', p[7])
    child8 = create_leaf('RPAREN', p[8])
    type = 'Array(' + str(p[7]) + ','+p[4].type + ')'
    temp = newtmp()
    #size = p[4].size * p[7]
    code = ['array,' +temp+',' +str(p[7])]
    p[0] = Node('array_initializer', [child1,child2,child3,p[4],child5,child6,child7,child8],type, None, None, code,temp)


def p_class_instance_creation_expression(p):
	''' class_instance_creation_expression : K_NEW ambiguous_name LPAREN argument_list_extras RPAREN '''
    #Sarthak will do this



def p_statement(p):
    '''  statement : statement_without_trailing_substatement
	                        | while_statement
	                        | if_then_else_statement
	                        | if_then_statement
                        | for_loop'''
    p[0] = Node('statement' , [p[1]], None,None,None,p[1].code,None)

def p_if_then_statement(p):
    #TODO creating new scope in all the following
    'if_then_statement : K_IF LPAREN expression RPAREN statement'
    child1 = create_leaf("K_IF", p[1])
    child2 = create_leaf("LPAREN", p[2])
    child3 = create_leaf("RPAREN", p[4])
    selse = newlabel()
    l1 = ["cmp, 0, " + p[3].place]
    l2 = ["je, " + selse]
    l3 = ["label," + selse]
    p[0] = Node("if_then_statement", [child1, child2, p[3], child3, p[5]], None, None, None, p[3].code + l1 + l2 + p[5].code + l3)

def p_if_then_else_statement(p):
    'if_then_else_statement : K_IF LPAREN expression RPAREN statement_no_short_if K_ELSE statement'
    'if_then_statement : K_IF LPAREN expression RPAREN statement'
    if(len(p) == 8):
        child1 = create_leaf("K_IF", p[1])
        child2 = create_leaf("LPAREN", p[2])
        child3 = create_leaf("RPAREN", p[4])
        child4 = create_leaf("K_ELSE", p[6])
        selse = newlabel()
        safter = newlabel()
        l1 = ["cmp, 0, " + p[3].place]
        l2 = ["je, " + selse]
        l3 = ["goto," + safter]
        l4 = ["label," + selse]
        l5 = ["label," + safter]
        p[0] = Node("if_then_statement", [child1, child2, p[3], child3, p[5], child4, p[7]], None, None, None, p[3].code + l1 + l2 + p[5].code + l3 + l4 + p[7].code + l5)
    else:
        child1 = create_leaf("K_IF", p[1])
        child2 = create_leaf("LPAREN", p[2])
        child3 = create_leaf("RPAREN", p[4])
        selse = newlabel()
        l1 = ["cmp, 0, " + p[3].place]
        l2 = ["je, " + selse]
        l3 = ["label," + selse]
        p[0] = Node("if_then_statement", [child1, child2, p[3], child3, p[5]], None, None, None, p[3].code + l1 + l2 + p[5].code + l3)

# what are the following three rules ??
def p_if_then_else_statement_no_short_if(p):
    'if_then_else_statement_no_short_if : K_IF LPAREN expression RPAREN statement_no_short_if K_ELSE statement_no_short_if'

def p_statement_no_short_if(p):
    '''  statement_no_short_if : statement_without_trailing_substatement
                                            | if_then_else_statement_no_short_if'''


def p_statement_without_trailing_substatement(p):
    '''  statement_without_trailing_substatement : block
                                                | switch
                                                | expression_statement
                                                | blank_statement
                                                | return_statement'''


    p[0] = Node("statement_without_trailing_subspace", [p[1]], code =p[1].code)


def p_blank_statement(p):
    'blank_statement : semi'
    p[0] = Node("blank_statement", [p[1]])

def p_empty(p):
    'empty :'
    p[0] = Node('empty', [], 'Unit',None,None,[])

def p_expression_statement(p):
    'expression_statement : statement_expression semi'
    p[0] = Node("expression_statement", [p[1], p[2]], None, None, None, p[1].code, p[1].place)


def p_statement_expression(p):
    ######what will be the place of method_invocation ?? Should be assigned later as temp.place() whenever  temp = func()
    '''  statement_expression : assignment
                                            | method_invocation
                                            | class_instance_creation_expression'''
    p[0] = Node("statement_expression", [p[1]], None, None, None, p[1].code, p[1].place)


def p_assignment(p):
    '''assignment : left_hand_side ASSIGN or_expression'''
    tas = ["=," + p[1].place + "," + p[3].place]
    child1 = create_leaf("ASSIGN", p[2])
    p[0] = Node("assignment", [p[1], child1, p[3]], None, None, None, p[1].code + p[3].code + tas)

def p_left_hand_side(p):
    #class and objects not supported in ambiguous name till now. Migght work for arrays
    '''left_hand_side : ambiguous_name
                            | array_invocation'''
    global CURR
    #array invocation not handled till now
    (x, y) = CURR.check_for_variable_declaration(p[1].val)
    if(x == 0):
        print("Correct the semantics")
        assert(false)
    else:
        holding_variable = str(y.id) + "_" + p[1].val
        p[0] = Node("left_hand_side", [p[1]], None, None, None, p[1].code, holding_variable)

#I think the default statement is missing !!
def p_switch(p):
    'switch : switch_header switch_body'
    exp = p[1].place
    code = []
    l = p[2].val.size()
    #?
    code += ["label," + p[2].val[0]]
    for i in [1..l - 1]:
        code += ["cmp, " + p[2].place + ", " + exp]
        code += ["je," + p[2].val[i]]
        code += ["label," + p[2].val[l]]
        p[0] = Node("switch", [p[1], p[2]], None, None, None, p[1].code + p[2].code + code)

def p_switch_header(p):
    '''switch_header : expression K_MATCH'''
    child = create_leaf("K_MATCH", p[2])
    p[0] = Node("switch_header", [p[1], child], None, None, None, p[1].code, p[1].place)

def p_switch_body(p):
    'switch_body : BLOCK_BEGIN multiple_inner_switch_statement  BLOCK_END'
    test = newlabel()
    next = p[2].val[0]
    vl = []
    pl = []
    vl.append(test)
    pl.append("$")
    child1 = create_leaf("BLOCK_BEGIN", p[1])
    child2 = create_leaf("BLOCK_END", p[3])
    l = p[2].place.size()
    for i in [1..l]:
        vl.append(p[2].val[i])
        pl.append(p[2].place[i])
        vl.append(next)
        p[0] = Node("switch_body", [child1, p[2], child2], None, None, vl, p[2].code, pl)

def p_multiple_inner_switch_statement(p):
    '''  multiple_inner_switch_statement : single_inner_switch_statement
                                                        | multiple_inner_switch_statement single_inner_switch_statement'''
    if(len(p) == 2):
        vl = []
        pl = []
        lab = newlabel()
        next = newlabel()
        vl.append(next)
        pl.append("$")
        vl.append(lab)
        pl.append(p[1].place)
        l1 = ["label," + lab]
        l2 = ["goto," + next]
        p[0] = Node("multiple_inner_switch", [p[1]], None, None, vl, l1 + p[1].code + l2, pl)

    else:
        vl = p[1].val
        pl = p[1].place
        lab = newlabel()
        vl.append(lab)
        pl.append(p[2].place)
        l1 = ["label," + lab]
        l2 = ["goto," + p[1].val[0]]
        p[0] = Node("multiple_inner_switch", [p[1], p[2]], None, None, vl, l1 + p[2].code + l2, pl)

def p_single_inner_switch_statement(p):
    '''single_inner_switch_statement : single_switch_statement_header single_switch_statement_body '''
    p[0] = Node("single_inner_switch_statement", [p[1], p[2]], None, None, None, p[1].code + p[2].code, p[1].place)

def p_single_switch_statement_body(p):
    '''single_switch_statement_body : expression
                                                    | block_statement_list'''
    p[0] = Node("single_switch_statement", [p[1]], None, None, None, p[1].code)

def p_single_switch_statement_header(p):
    'single_switch_statement_header : K_CASE expression IMPLIES'
    child1 = create_leaf("K_CASE", p[1])
    child2 = create_leaf("IMPLIES", p[3])
    p[0] = Node("single_switch_statement_header", [child1, p[2], child2], None, None, None, p[2].code, p[2].place)


def p_while_statement(p):
    'while_statement : K_WHILE LPAREN expression RPAREN statement'
    s_begin = newlabel()
    s_after = newlabel()
    child1 = create_leaf("K_WHILE", p[1])
    child2 = create_leaf("LPAREN", p[2])
    child3 = create_leaf("RPAREN", p[4])
    l1 = ["label," + s_begin]
    l2 = ["cmp, 0, " + p[3].place]
    l3 = ["je, " + s_after]
    l4 = ["goto, " + s_begin]
    l5 = ["label, " + s_after]
    p[0] = Node("while_statement", [child1, child2, p[3], child3, p[5]], None, None, None, l1 + p[3].code + l2 + l3 + p[5].code + l4 + l5)

#Leave the for loop for later
def p_for_loop(p):
    #TODO : create a new scope and push the iterator in the symbol table of the scope
    'for_loop : K_FOR LPAREN for_variables  RPAREN statement'
    child1 = create_leaf("K_FOR", p[1])
    child2 = create_leaf("LPAREN", p[2])
    child3 = create_leaf("RPAREN", p[3])
    type = p[3].val[0]
    to_until = p[3].val[1]
    if(to_until == 0): sym = "jge"
    else: sym = "jg"
    s_begin = newlabel()
    s_after = newlabel()
    if(type == 0):
        #two expressions in the for statement
        iterator = newtmp()
        exp1 = p[3].val[2]
        exp2 = p[3].val[3]
        l1 = ["=," + iterator + "," + exp1]
        l2 = ["label," + s_begin]
        l3 = ["cmp, " + exp2 + "," + iterator]
        l4 = [sym + "," + s_after]
        l7 = ["+," + counter + "," + counter]
        l5 = ["goto," + s_begin]
        l6 = ["label," + s_after]
        p[0] = Node("for_loop", [child1 + child2 + p[3] + child3 + p[5]], None, None, None, [p[3].code + l1 + l2 + l3+ l4 + p[5].code + l7 + l5 + l6])
    else:
        pass


def p_for_variables(p):
    ''' for_variables : declaration_keyword_extras IDENTIFIER IN expression for_untilTo expression '''

def p_declaration_keyword_extras(p):
    '''declaration_keyword_extras : variable_header
                                    | empty'''
def p_for_untilTo(p):
    '''  for_untilTo : K_UNTIL
                        | K_TO'''

def p_return_statement(p):
    '''return_statement : K_RETURN expression semi
                                    | K_RETURN semi'''

#types
def p_type(p):
    '''type : basic_type
                | array_datatype '''
    p[0] = Node("type", [p[1]], p[1].type, None, p[1].type,None,None)

def p_basic_type(p):
    '''basic_type : K_CHAR
                             | K_UNIT
                             | K_FLOAT
                             | K_STRING
                             | K_BOOLEAN
                             | K_INT'''
    child = create_leaf('Type' , p[1])
    p[0] = Node("basic_type", [child], p[1], None, None,None,None)


# def p_other_type(p):
#     '''other_type : nonarray_datatype
#                         | array_datatype'''

def p_array_datatype(p):
    '''array_datatype : K_ARRAY square_block
                                | K_LIST square_block'''
    child = create_leaf('Array/List', p[1])     
    p[0] = Node('array_datatype', [child, p[2]], 'Array['+p[2].type+']' )                           

def p_square_block(p):
    ''' square_block : SQUARE_BEGIN type SQUARE_END'''
    child1 = create_leaf('SQUARE_BEGIN', p[1])
    child2 = create_leaf('SQUARE_END', p[3])
    p[0] = Node('square_block', [child1, p[2],child2], p[2].type, None,None,None,None)


logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w"
)

log = logging.getLogger()
parser = yacc.yacc()
if __name__ == "__main__" :
    
    file = (open(sys.argv[1],'r')).read()
    file+= "\n"
    result = parser.parse(file,debug=log)
    rules_raw = open("rules_used.txt",'w')
    for line in open("parselog.txt",'r').readlines():
        if re.match("INFO:root:Action(.*)", line):
            rules_raw.write(line)


    rules_raw.close();
                #Clean the garbage words
    rules_raw = "rules_used.txt"
    rules_clean = "reverse_actions.txt"
    fin = open(rules_raw)
    fout = open(rules_clean, "w+")
    for line in fin:
        matched_line = re.findall('rule \[(.*)\] with', line)
        fout.write(matched_line[0])
        fout.write("\n")
    fin.close()
    fout.close()
    os.remove("rules_used.txt")
