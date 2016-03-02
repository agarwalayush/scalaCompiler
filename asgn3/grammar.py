# from symbolTable import *
# SCOPE = Env(None)                          # Current Scope

import ply.yacc as yacc
import sys
import logging

# Get the token map from the lexer.  This is required.
#from lexer import tokens
from lexer import tokens

def p_compilation_unit(p):
    'compilation_unit :  import_declarations_opts classes_objects'

def p_import_declarations_opts(p):
  '''import_declarations_opts : import_declarations
                                          | empty'''

def p_import_declarations(p):
    '''import_declarations :  import_declaration
                                      | import_declarations import_declaration'''

def p_import_declaration(p):
    '''import_declaration :  K_IMPORT expression_name'''


def p_classes_objects(p):
    '''classes_objects : classes_objects  class_and_objects
                      | class_and_objects '''

def p_class_and_objects(p):
  '''class_and_objects : object_declaration
                       | class_declaration'''

def p_object_declaration(p):
    'object_declaration : ObjectDeclare block'


# object declaration
def p_object_declare(p):
    '''ObjectDeclare : K_OBJECT IDENTIFIER super '''

def p_class_type(p):
  '''class_type : IDENTIFIER
                    | K_WITH class_type'''

def p_super(p):
  '''super : K_EXTENDS class_type
              | empty'''


def p_class_declaration(p):
        '''class_declaration : class_header class_body'''

def p_class_header(p):
        '''class_header : K_CLASS IDENTIFIER LPAREN constructor_arguement_list_opt RPAREN super'''

def p_class_body(p):
        '''class_body : BLOCK_BEGIN class_body_declarations_opts BLOCK_END '''

                                    ####---testing---###

def p_class_body_declarations_opts(p):
      '''class_body_declarations_opts : class_body_declarations
                                                    | empty'''

def p_class_body_declarations(p):
    '''class_body_declarations : class_body_declaration
                                          | class_body_declarations class_body_declaration'''

def p_class_body_declaration(p):
    '''class_body_declaration : field_declaration
                                          | method_declaration'''

def p_field_declaration(p):
    'field_declaration :   declaration_keyword variable_declaration_body  semi'

def p_semi(p):
    '''semi : SEMI_COLON
                | NEWLINE'''

# def p_val_var_opts(p):
#     ''' val_var_opts : val
#                         | empty'''

# def p_val(p):
#     '''  val : K_VAL
#        | K_VAR'''

# def p_variable_declarators(p):
#       '''variable_declarators : variable_declarator
#                                 | variable_declarators COMMA variable_declarator'''

# def p_variable_declarator(p):
#     '''variable_declarator :  IDENTIFIER
#                                 |  IDENTIFIER COLON type
#                                 | IDENTIFIER variable_declarator_extra  '''

# def p_variable_declarator_extra(p):
#     '''variable_declarator_extra :  ASSIGN variable_initializer
#                                         | COLON type ASSIGN variable_initializer'''

# def p_variable_initializer(p):
#     '''variable_initializer :  expression
#                             | array_initializer'''

# def p_method_declaration(p):
#     'method_declaration :  method_header method_body'

# def p_method_header(p):         #####
#     '''method_header :  K_DEF method_declarator COLON type ASSIGN
#                         | K_DEF method_declarator ASSIGN
#                         | K_DEF method_declarator'''

# def p_method_declarator(p):
#     'method_declarator :  IDENTIFIER LPAREN formal_parameter_list RPAREN'

# def p_method_body(p):
#     '''method_body :  block
#                     | semi'''

                                      ####---testing---###

def p_constructor_arguement_list_opt(p):
  '''constructor_arguement_list_opt : constructor_arguement_list
                            | empty '''


def p_constructor_arguement_list(p):
  '''constructor_arguement_list : constructor_arguement_list_declarator
                         | constructor_arguement_list COMMA constructor_arguement_list_declarator'''

def p_constructor_arguement_list_declarator(p):
    '''constructor_arguement_list_declarator : IDENTIFIER COLON type'''  #removed declaration_keyword

def p_func_arguement_list_opt(p):
  '''func_arguement_list_opt : variable_declarators
                            | empty '''


def p_method_declaration(p):
        '''method_declaration : method_header method_body'''


def p_method_header(p):
        '''method_header : K_DEF IDENTIFIER LPAREN func_arguement_list_opt RPAREN method_return_type_opt '''

def p_method_return_type_opt(p):
  '''method_return_type_opt : COLON method_return_type ASSIGN
                                          | ASSIGN
                                          | empty'''

def p_method_return_type(p):
        '''method_return_type : type
                                        | K_UNIT'''

def p_method_body(p):
        '''method_body : block '''

# def p_modifier(p):
#       '''modifier : K_PROTECTED
#                   | K_PRIVATE'''


def p_type(p):
        '''type : primitive_type
                | reference_type '''

def p_primitive_type(p):
    '''primitive_type : K_INT
                      | K_FLOAT
                      | K_CHAR
                      | K_STRING
                      | K_BOOLEAN'''


def p_reference_type(p):
      '''reference_type : class_data_type
                        | array_data_type'''

def p_class_data_type(p):
      '''class_data_type : IDENTIFIER'''

def p_array_data_type(p):
      '''array_data_type : K_ARRAY SQUARE_BEGIN type SQUARE_END'''

def p_array_initializer(p):
  ''' array_initializer : K_NEW K_ARRAY SQUARE_BEGIN type SQUARE_END LPAREN INT RPAREN
                            | K_ARRAY LPAREN argument_list_opt RPAREN '''


def p_class_instance_creation_expression(p):
  ''' class_instance_creation_expression : K_NEW class_data_type LPAREN argument_list_opt RPAREN '''


# expression
def p_expression(p):
    '''expression : assignment_expression'''


def p_expression_optional(p):
        '''expression_optional : expression
                          | empty'''

def p_assignment_expression(p):
    '''assignment_expression : assignment
                             | conditional_or_expression'''

# assignment

def p_assignment(p):
    '''assignment : left_hand_side assignment_operator assignment_expression'''


def p_assignment_operator(p):
    '''assignment_operator :    ASSIGN'''
# OR(||) has least precedence, and OR is left assosiative
# a||b||c => first evalutae a||b then (a||b)||c

def p_conditional_or_expression(p):
    '''conditional_or_expression : conditional_and_expression
                                | conditional_or_expression OR conditional_and_expression'''

# AND(&&) has next least precedence, and AND is left assosiative
# a&&b&&c => first evalutae a&&b then (a&&b)&&c

def p_conditional_and_expression(p):
    '''conditional_and_expression : exclusive_or_expression
                                    | conditional_and_expression AND exclusive_or_expression'''

# def p_inclusive_or_expression(p):
#     '''inclusive_or_expression : exclusive_or_expression
#                                    | inclusive_or_expression OR_BITWISE exclusive_or_expression'''

def p_exclusive_or_expression(p):
    '''exclusive_or_expression : equality_expression
                                   | exclusive_or_expression XOR equality_expression'''


def p_equality_expression(p):
    '''equality_expression : relational_expression
                            | equality_expression EQUAL relational_expression
                            | equality_expression NEQUAL relational_expression'''


def p_relational_expression(p):
    '''relational_expression : additive_expression
                                 | relational_expression GREATER_THAN additive_expression
                                 | relational_expression LESS_THAN additive_expression
                                 | relational_expression GREATER_THAN_EQUAL additive_expression
                                 | relational_expression LESS_THAN_EQUAL additive_expression'''


def p_additive_expression(p):
    '''additive_expression : multiplicative_expression
                               | additive_expression PLUS multiplicative_expression
                               | additive_expression MINUS multiplicative_expression'''

def p_multiplicative_expression(p):
    '''multiplicative_expression : unary_expression
                                     | multiplicative_expression MULT unary_expression
                                     | multiplicative_expression DIVIDE unary_expression
                                     | multiplicative_expression MOD unary_expression'''


def p_unary_expression(p):
    '''unary_expression : PLUS unary_expression
                            | MINUS unary_expression
                            | unary_expression_not_plus_minus'''

def p_unary_expression_not_plus_minus(p):
    '''unary_expression_not_plus_minus : postfix_expression
                                           | NOT unary_expression'''
                                           # | TILDA unary_expression

def p_postfix_expression(p):
    '''  postfix_expression : primary_no_new_array
                                    | expression_name'''

def p_primary_no_new_array(p):
    '''  primary_no_new_array : literal
                                        | LPAREN expression RPAREN
                                        | method_invocation
                                        | array_access'''


# def p_base_variable_set(p):
#   '''base_variable_set : variable_literal
#                         | LPAREN expression RPAREN'''

# def p_cast_expression(p):
#         '''cast_expression : LPAREN primitive_type RPAREN unary_expression'''

# def p_primary(p):
#     '''primary : literal
#                 | method_invocation'''

def p_literal(p):
  '''literal : STRING
              | CHAR
              | K_FALSE
              | K_TRUE
              | K_NULL
              | FLOAT
              | INT'''

def p_method_invocation(p):
    '''method_invocation : expression_name LPAREN argument_list_opt RPAREN '''

def p_array_access(p):
    '''array_access : expression_name SQUARE_BEGIN expression SQUARE_END '''


def p_argument_list_opt(p):
    '''argument_list_opt : argument_list
                                    | empty'''


def p_argument_list(p):
    '''argument_list : expression
                    | argument_list COMMA expression'''

def p_expression_name(p):
    '''expression_name : IDENTIFIER
                        | ambiguous_name DOT IDENTIFIER'''

def p_ambiguous_name(p):
    '''ambiguous_name : IDENTIFIER
                        | ambiguous_name DOT IDENTIFIER'''

def p_left_hand_side(p):
    '''left_hand_side : expression_name
                      | array_access'''


# def p_variableliteral(p):
#     '''variable_literal : left_hand_side
#                         | primary'''

# BLOCK STATEMENTS


def p_block(p):
      '''block : BLOCK_BEGIN block_statements_opt BLOCK_END '''


def p_block_statements_opt(p):
      '''block_statements_opt : block_statements
                                          | empty'''

def p_block_statements(p):
      '''block_statements : block_statement
                                    | block_statements block_statement'''

def p_block_statement(p):
      '''block_statement : local_variable_declaration_statement
                           | statement
                           | method_declaration'''
                           # | class_declaration
                           # | object_declaration

# var (a:Int)=(h);
# var (a:Int,b:Int,c:Int)=(1,2,3);
# var (a:Int)=(h)
# var (a:Int,b:Int,c:Int)=(1,2,3)
# supported

# def p_modifier_opts(p):
#   '''modifier_opts : modifier
#                     | empty '''

def p_declaration_keyword(p):
  '''declaration_keyword : K_VAR
                         | K_VAL '''


def p_local_variable_declaration_statement(p):
      '''local_variable_declaration_statement : local_variable_declaration  semi '''

#
def p_local_variable_declaration(p):
      '''local_variable_declaration : declaration_keyword variable_declaration_body'''  #removed modifier opts


def p_variable_declaration_initializer(p):
  '''variable_declaration_initializer : expression
                                      | array_initializer
                                      | class_instance_creation_expression'''

# def p_variable_arguement_list(p):
#   ''' variable_arguement_list : variable_declaration_initializer
#                     | variable_arguement_list COMMA variable_declaration_initializer'''

def p_variable_declaration_body(p):
      '''variable_declaration_body : variable_declarator  ASSIGN  variable_declaration_initializer '''

# def p_variable_declaration_body_2(p):
#       '''variable_declaration_body : LPAREN variable_declarators RPAREN ASSIGN LPAREN variable_arguement_list RPAREN'''

#left
def p_variable_declaration_body_3(p):
  ''' variable_declaration_body : IDENTIFIER ASSIGN LPAREN func_arguement_list_opt RPAREN FUNTYPE expression'''

def p_variable_declarators(p):
      '''variable_declarators : variable_declarator
                                | variable_declarators COMMA variable_declarator'''

def p_variable_declarator(p):
      '''variable_declarator : IDENTIFIER COLON type'''
        # '''variable_declarator : IDENTIFIER  '''



# def p_variable_declarator_id(p):
#       '''variable_declarator_id : IDENTIFIER COLON type'''

def p_statement(p):
        '''statement : normal_statement
                     | if_then_statement
                     | if_then_else_statement
                     | while_statement
                     | do_while_statement
                     | for_statement'''


def p_normal_statement(p):
        '''normal_statement : block
                             | expression_statement
                             | empty_statement
                             | return_statement
                             | switch_statement'''

def p_expression_statement(p):
        '''expression_statement : statement_expression  semi'''


def p_statement_expression(p):
        '''statement_expression : assignment
                                | method_invocation'''

def p_if_then_statement(p):
        '''if_then_statement : K_IF LPAREN expression RPAREN statement'''

def p_if_then_else_statement(p):
        '''if_then_else_statement : K_IF LPAREN expression RPAREN if_then_else_intermediate K_ELSE statement'''


def p_if_then_else_statement_precedence(p):
        '''if_then_else_statement_precedence : K_IF LPAREN expression RPAREN if_then_else_intermediate K_ELSE if_then_else_intermediate'''

def p_if_then_else_intermediate(p):
        '''if_then_else_intermediate : normal_statement
                                     | if_then_else_statement_precedence'''


def p_while_statement(p):
        '''while_statement : K_WHILE LPAREN expression RPAREN statement'''

def p_do_while_statement(p):
        '''do_while_statement : K_DO statement K_WHILE LPAREN expression RPAREN  semi '''

def p_for_statement(p):
  '''for_statement : K_FOR LPAREN for_logic RPAREN statement'''

def p_for_logic(p):
    ''' for_logic : for_loop
                  | for_loop  semi for_logic '''

    #changed here

# def p_for_update(p):
#   ''' for_update : for_loop  '''  #changed here

def p_for_loop(p):
  ''' for_loop : IDENTIFIER IN expression for_untilTo expression '''

def p_for_untilTo(p):
  '''for_untilTo : K_UNTIL
                  | K_TO'''


# def p_for_step_opts(p):
#   ''' for_step_opts : K_BY expression
#                     | empty'''


def p_switch_statement( p):
        '''switch_statement : expression K_MATCH switch_block '''


def p_switch_block(p):
        '''switch_block : BLOCK_BEGIN BLOCK_END '''

def p_switch_block2(p):
        '''switch_block : BLOCK_BEGIN switch_block_statements BLOCK_END '''

def p_switch_block3(p):
        '''switch_block : BLOCK_BEGIN switch_labels BLOCK_END '''


def p_switch_block4(p):
        '''switch_block : BLOCK_BEGIN switch_block_statements switch_labels BLOCK_END '''

def p_switch_block_statements(p):
        '''switch_block_statements : switch_block_statement
                                   | switch_block_statements switch_block_statement'''

def p_switch_block_statement(p):
        '''switch_block_statement : switch_labels block_statements'''


def p_switch_labels(p):
        '''switch_labels : switch_label
                         | switch_labels switch_label'''


def p_switch_label(p):
        '''switch_label : K_CASE expression FUNTYPE '''


def p_empty_statement(p):
        '''empty_statement :  semi '''

def p_return_statement(p):
        '''return_statement : K_RETURN expression_optional  semi '''


def p_empty(p):
    'empty :'
    pass


logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w"
)

log = logging.getLogger()
parser = yacc.yacc()


if __name__ == "__main__" :

    s = open(sys.argv[1],'r')
    data = s.read()
    data+= "\n"
    s.close()
    result = parser.parse(data,debug=log)


    import re
    from collections import defaultdict

    #obtain the lines with the productions used
    outfile = open("actions.txt",'w')
    with open("parselog.txt") as f:
        for line in f:
            if re.match("INFO:root:Action(.*)", line):
                outfile.write(line)


    #clean the productions to give the required information
    infile = "actions.txt"
    outfile = "treefile.txt"

    delete_list2 = ["rule [","] with"]

    fin = open(infile)
    fout = open(outfile, "w+")
    for line in fin:
       matches = re.findall('rule \[(.*)\] with', line)
       #for word in delete_list2:
       #    matches[0] = matches[0].replace(word, "")
       fout.write(matches[0])
       #line = line[1:len(line)-2]
       #fout.write(line)
       fout.write("\n")
    fin.close()
    fout.close()



    #use the clean productions and build the dot file
    nodes = defaultdict(list)
    #nodes = dict()
    nodeNum = 1

    # infile = sys.argv[1]
    # outfile = infile[0:len(infile)-3]
    outfile="out.dot"
    # outfile = outfile.split("/")[-1]

    fout = open(outfile,"w")

    fout.write("""digraph G {
    graph [ordering="out"];
    """)
    fout.write("\n")

    for line in open("treefile.txt"):
        columns = line.split(" ")
        fout.write("node%d [ label = \"%s\" ]; " % (nodeNum,columns[0]))
        fout.write("\n")
        lhsNum = nodeNum
        nodeNum += 1
        edges = []
        for i in range(1,len(columns)-1):
            i = len(columns)  - i
        columns[i] = columns[i].rstrip()
        edge = ""
        if columns[i] in nodes:
            edge += "node" + str(lhsNum) + " -> node" + str(nodes[columns[i]].pop(len(nodes[columns[i]])-1)) + ";"
            if len(nodes[columns[i]]) == 0:
               del nodes[columns[i]]
        else:
            fout.write("node%d [ label = \"Token \n %s\" ]; " % (nodeNum,columns[i]))
            fout.write("\n")
            edge += "node" + str(lhsNum) + " -> node" + str(nodeNum) + ";"
            #print "node%d -> node%d;" %(lhsNum,nodeNum)
            nodeNum += 1
        edges.append(edge)
        nodes[columns[0]].append(lhsNum)
        while edges:
           fout.write(edges.pop(len(edges)-1))
           fout.write("\n")

    fout.write( "}" )
    fout.write("\n")
    fout.close()

