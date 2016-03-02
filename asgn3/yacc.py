# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lexer import tokens



class Node:
    def __init__(self,label,children=None, type = 'Unit'):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = [ ]
        self.label= label
    def mkleaf(name, value, type='Unit'):
        child = Node(value,[],type)
        parent = Node(name, [child],type)
        return parent


def p_compilation_unit(p):
    'compilation_unit :  import_declarations classes_objects'

def p_import_declarations(p):
    '''import_declarations :  import_declaration
                                            | import_declarations import_declaration'''

def p_import_declaration(p):
    'import_declaration :  K_IMPORT type'

def p_classes_objects(p):
    '''classes_objects :  class_object
                        | class_object classes_objects'''

def p_class_object(p):
    '''class_object :  class_declaration
                                | object_declaration
                                | semi'''

def p_semi(p):
        ''' semi : SEMI_COLON
                    | empty'''

def p_object_declaration(p):
    'object_declaration :  K_OBJECT IDENTIFIER super BLOCK_BEGIN method_body BLOCK_END'

def p_class_declaration(p):
    'class_declaration :  K_CLASS IDENTIFIER class_header super BLOCK_BEGIN class_body_declarations BLOCK_END'

def p_super(p):
    '''super :  K_EXTENDS class_type
                        | empty'''

def p_class_header(p):
    'class_header :  LPAREN formal_parameter_list RPAREN'

def p_class_body_declarations(p):
    '''class_body_declarations : class_body_declaration
                                                    | class_body_declarations class_body_declaration
                                                    | empty'''

def p_class_body_declaration(p):
    '''class_body_declaration : field_declaration
                                                | method_declaration'''

def p_formal_parameter_list(p):
    '''formal_parameter_list : formal_parameter
                                                | formal_parameter_list COMMA formal_parameter
                                                | empty'''

def p_variable_declarator_id(p):
      '''variable_declarator_id : IDENTIFIER COLON type'''

def p_formal_parameter(p):
    'formal_parameter : variable_declarator_id COLON type'

def p_class_type(p):
    '''class_type : IDENTIFIER
                        | K_WITH identifierclass_type'''

def p_field_declaration(p):
    'field_declaration :   val variable_declarator SEMI_COLON'

def p_val(p):
    '''  val : K_VAL
       | K_VAR'''

def p_variable_declarators(p):
      '''variable_declarators : variable_declarator
                                | variable_declarators COMMA variable_declarator'''

def p_variable_declarator(p):
    '''variable_declarator :  IDENTIFIER
                                |  IDENTIFIER COLON type
                                | IDENTIFIER variable_declarator_extra  '''

def p_variable_declarator_extra(p):
    '''variable_declarator_extra :  ASSIGN variable_initializer
                                        | COLON type ASSIGN variable_initializer'''

def p_variable_initializer(p):
    '''variable_initializer :  expression
                            | array_initializer'''

def p_method_declaration(p):
    'method_declaration :  method_header method_body'

def p_method_header(p):
    '''method_header :  K_DEF method_declarator COLON type ASSIGN
                            | K_DEF method_declarator ASSIGN '''

def p_method_declarator(p):
    'method_declarator :  IDENTIFIER LPAREN formal_parameter_list RPAREN'

def p_method_body(p):
    '''method_body :  block
                    | semi'''



def p_type(p):
    '''type : primitive_type
            | reference_type'''

def p_primitive_type(p):
    '''primitive_type : numeric_type
                    | K_BOOLEAN'''

def p_numeric_type(p):
    '''numeric_type : integral_type
                    | floating_point_type'''

def p_integral_type(p):
    '''integral_type : INT
                    | LONG
                    | CHAR'''

def p_floating_point_type(p):
    '''floating_point_type : FLOAT'''

def p_reference_type(p):
    '''reference_type : class_type
                        | array_type'''
def p_array_type(p):
    '''array_type : type SQUARE_BEGIN SQUARE_END'''

def p_array_initializer(p):
  ''' array_initializer : K_NEW K_ARRAY SQUARE_BEGIN type SQUARE_END LPAREN INT RPAREN
                        | K_ARRAY LPAREN argument_list_optional RPAREN '''


#BLOCKS AND COMMANDS
#---------------------------------------

def p_block(p):
    '''block : BLOCK_BEGIN block_statements BLOCK_END
                | BLOCK_BEGIN BLOCK_END'''
    child1 = mkleaf("BLOCK_BEGIN" , '{')
    child2 = mkleaf("BLOCK_BEGIN" , '}')
    if(len(p) == 2):
        p[0] = Node("Block" , [child1,child2])
    else:
        p[0] = Node("Block" , [child1,p[2],child2])

def p_block_statements(p):
    '''  block_statements : block_statement
             | block_statements block_statement'''
    if len(p) == 2:
        p[0] = Node("block_statements", [p[1]])
    else:
        p[0] = Node("block_statements", [p[1], p[2]])

def p_block_statement(p):
    '''  block_statement : local_variable_declaration_statement
             | statement'''
    p[0] = Node("block statement" , [p[1]]) 

def p_local_variable_declaration_statement(p):
    'local_variable_declaration_statement : variable_declarators semi'
    p[0] = Node("local_variable_declaration_statement " , [p[1], p[2]]) 

def p_statement(p):
    '''  statement : statement_without_trailing_substatement
                        | if_then_statement
                        | if_then_else_statement
                        | while_statement
                        | for_loop'''
    p[0] = Node("statement " , [p[1]]) 

def p_statement_without_trailing_substatement(p):
    '''  statement_without_trailing_substatement : block
             | empty_statement 
                                     | expression_statement 
                                     | switch_statement 
                                     | return_statement'''
    p[0] = Node("statement_without_trailing_substatement " , [p[1]]) 

def p_statement_no_short_if(p):
    '''  statement_no_short_if : statement_without_trailing_substatement
             | if_then_else_statement_no_short_if'''
    p[0] = Node("statement_no_short_if " , [p[1]])

def p_empty_statement(p):
    'empty_statement : semi'
    p[0] = Node("empty_statement " , [p[1]])

def p_empty(p):
    'empty : '
    child = mkleaf("empty", '')
    p[0] =  Node("empty" , [child])

def p_expression_statement(p):
    'expression_statement : statement_expression semi'
    p[0] = Node("expression_statement " , [p[1], p[2]])

def p_statement_expression(p):
    '''  statement_expression : assignment
            | method_invocation 
                                    | class_instance_creation_expression'''
    p[0] = Node("statement_expression " , [p[1]])

def p_if_then_statement(p):
    'if_then_statement : K_IF LPAREN expression RPAREN statement'
    child1 = mkleaf("K_IF", p[1])
    child2 = mkleaf("LPAREN", p[2])
    child4 = mkleaf("RPAREN", p[4])
    p[0] = Node("if_then_statement" , [child1, child2, p[3], child4, p[5]])

def p_if_then_else_statement(p):
    'if_then_else_statement : K_IF LPAREN expression RPAREN statement_no_short_if K_ELSE statement'
    child1 = mkleaf("K_IF", p[1])
    child2 = mkleaf("LPAREN", p[2])
    child4 = mkleaf("RPAREN", p[4])
    child6 = mkleaf("K_ELSE", p[6])
    p[0] = Node("if_then_else_statement" , [child1, child2, p[3], child4, p[5],child6, p[7]])

def p_if_then_else_statement_no_short_if(p):
    'if_then_else_statement_no_short_if : K_IF LPAREN expression RPAREN statement_no_short_if K_ELSE statement_no_short_if'
    child1 = mkleaf("K_IF", p[1])
    child2 = mkleaf("LPAREN", p[2])
    child4 = mkleaf("RPAREN", p[4])
    child6 = mkleaf("K_ELSE", p[6])
    p[0] = Node("if_then_else_statement_no_short_if " , [child1, child2, p[3], child4, p[5],child6, p[7]])

def p_switch_statement(p):
    'switch_statement : expression  K_MATCH switch_block'
    child1 = mkleaf("K_MATCH", p[2])
    p[0] = Node("switch_statement " , [p[1], child1, p[3]])

def p_switch_block(p):
    'switch_block : BLOCK_BEGIN switch_block_statement_groups_optional switch_labels_optional BLOCK_END'
    child1 = mkleaf("BLOCK_BEGIN ", p[1])
    child4 = mkleaf("BLOCK_END", p[4])
    p[0] = Node("switch_block " , [child1, p[2], p[3], child4])

def p_switch_block_statement_groups_optional(p):
    '''  switch_block_statement_groups_optional : switch_block_statement_groups
             | empty'''
    p[0] = Node("switch_block_statement_groups_optional " , [p[1]])

def p_switch_labels_optional(p):
    '''  switch_labels_optional : switch_labels
             | empty'''
    p[0] = Node("switch_labels_optional" , [p[1]])

def p_switch_block_statement_groups(p):
    '''  switch_block_statement_groups : switch_block_statement_group
             | switch_block_statement_groups switch_block_statement_group'''
    if len(p) == 2:
        p[0] = Node("switch_block_statement_groups ", [p[1]])
    else:
        p[0] = Node("switch_block_statement_groups ", [p[1], p[2]])

def p_switch_block_statement_group(p):
    'switch_block_statement_group : switch_labels block_statements'
    p[0] = Node("switch_block_statement_group " , [p[1], p[2]])

def p_switch_labels(p):
    '''  switch_labels : switch_label
             | switch_labels switch_label'''
    if len(p) == 2:
        p[0] = Node("switch_labels ", [p[1]])
    else:
        p[0] = Node("switch_labels ", [p[1], p[2]])

def p_switch_label(p):
    'switch_label : K_CASE expression COLON'
    child1 = mkleaf("K_CASE", p[1])
    child2 = mkleaf("COLON", p[2])
    p[0] = Node("switch_label ", [child1,p[2], child2])

def p_while_statement(p):
    'while_statement : K_WHILE LPAREN expression RPAREN statement'
    child1 = mkleaf("K_WHILE ", p[1])
    child2 = mkleaf("LPAREN", p[2])
    child4 = mkleaf("RPAREN", p[4])
    p[0] = Node("while_statement " , [child1, child2, p[3], child4, p[5]])

def p_for_loop(p):
    'for_loop : K_FOR BLOCK_BEGIN for_exprs for_if_condition BLOCK_END statement'
    child1 = mkleaf("K_FOR ", p[1])
    child2 = mkleaf("BLOCK_BEGIN ", p[2])
    child5 = mkleaf("BLOCK_END", p[4])
    p[0] = Node("for_loop" , [child1, child2, p[3], p[4], child5, p[6]])


def p_for_if_condition(p):
    '''for_if_condition : SEMI_COLON if_variables  for_if_condition
                            | if_variables'''
    child1 = mkleaf("SEMI_COLON ", p[1])
    if(len(p) == 2):
        p[0] = Node("for_if_condition" , [p[1]])
    else:
        p[0] = Node("for_if_condition" , [child1, p[2], p[3]])

def p_if_variables(p):
    'if_variables : K_IF expression '
    child1= mkleaf("K_IF", p[1])
    p[0]= Node("if_variables ", [child1, p[2]])

def p_for_exprs(p):
    '''for_exprs :  for_variables SEMI_COLON for_exprs
                    | for_variables'''
    if(len(p)==2):
        p[0]= Node("for_exprs", [p[1]])
    else:
        child = mkleaf("SEMI_COLON", p[2])
        p[0]= Node("for_exprs ", [p[1],child, p[3]])

def p_for_variables(p):
    'for_variables : IDENTIFIER IN expression for_untilTo expression '

    child1 = mkleaf("IDENTIFIER", p[1])
    child2 = mkleaf("IN", p[2])
    p[0] = Node("for_variables", [child1,child2, p[3],p[4],p[5]])

def p_for_untilTo(p):
    '''  for_untilTo : K_UNTIL
        | K_TO'''
    child = mkleaf("UNTIL/TO", p[1])
    p[0] = Node("for_untilTo", [child])

def p_return_statement(p):
    '''return_statement : K_RETURN expression semi
                                | K_RETURN semi'''
    child = mkleaf("K_RETURN", p[1])
    if(len(p) == 3):
        p[0]= Node("return_statement",[child , p[2]])
    else:
        p[0]= Node("return_statement",[child , p[2],p[3]])        


#EXPRESSIONS!
#---------------------------------------
def p_expression(p):
    'expression : assignment_expression'
    p[0] = Node("expression" , [p[1]] , p[1].type)

def p_assignment_expression(p):
    '''  assignment_expression : conditional_expression
             | assignment'''
    p[0] = Node("assignment_expression" , [p[1]], p[1].type)

def p_assignment(p):
    'assignment : left_hand_side assignment_operator assignment_expression'
    if(p[1].type != p[3].type):
        raise TypeError
    p[0] = Node("assignment" , [p[1] , p[2], p[3]], p[1].type)

def p_left_hand_side(p):
    '''  left_hand_side : expression_name
             | array_access'''
    p[0] = Node("left_hand_side", [p[1]], p[1].type)



def p_assignment_operator(p):
    'assignment_operator : ASSIGN'
    child = mkleaf("ASSIGN" , p[1])
    p[0] = Node("assignment_operator", [child])

def p_conditional_expression_1(p):          #what's this ?????
    '''  conditional_expression : conditional_or_expression
            |  conditional_or_expression  expression COLON conditional_expression
                                    | expression COLON conditional_expression'''
    if(len(p) == 2):
        p[0] = Node("conditional_expression", [p[1]] , p[1].type) 
    elif(len(p) == 4):
        child = mkleaf("COLON" , p[2])
        p[0] = Node("conditional_expression", [p[1] , child , p[3]] , p[1].type) 
    else:
        child = mkleaf("COLON" , p[3])
        p[0] = Node("conditional_expression", [p[1] , p[2], child , p[4]] , p[1].type) 

# def p_conditional_expression_2(p):
#       conditional_expression : conditional_or_expression
#            | expression COLON conditional_expression'''

def p_conditional_or_expression(p):
    '''  conditional_or_expression : conditional_and_expression
             | conditional_or_expression OR conditional_and_expression'''

def p_conditional_and_expression(p):
    '''  conditional_and_expression : inclusive_or_expression
             | conditional_and_expression AND inclusive_or_expression'''

def p_inclusive_or_expression(p):
    'inclusive_or_expression : exclusive_or_expression'

def p_exclusive_or_expression(p):
    'exclusive_or_expression : and_expression'

def p_and_expression(p):
    ' and_expression : equality_expression'

def p_equality_expression(p):
    '''  equality_expression : relational_expression
             | equality_expression EQUAL relational_expression
                                     | equality_expression NEQUAL relational_expression'''

def p_relational_expression(p):
    '''  relational_expression : shift_expression
             | relational_expression LESS_THAN shift_expression
                                    | relational_expression GREATER_THAN shift_expression
                                    | relational_expression LESS_THAN_EQUAL shift_expression
                                    | relational_expression GREATER_THAN_EQUAL shift_expression'''

def p_shift_expression(p):
    'shift_expression : additive_expression '

def p_additive_expression(p):
    '''  additive_expression : multiplicative_expression
             | additive_expression PLUS multiplicative_expression
                                    | additive_expression MINUS multiplicative_expression'''

def p_multiplicative_expression(p):
    '''  multiplicative_expression : unary_expression
             | multiplicative_expression MULT unary_expression
                                    | multiplicative_expression DIVIDE unary_expression
                                    | multiplicative_expression MOD unary_expression'''

def p_cast_expression(p):
    'cast_expression : LPAREN primitive_type RPAREN unary_expression '

def p_unary_expression(p):
    '''unary_expression :  PLUS unary_expression
                                    | MINUS unary_expression
                                    | unary_expression_not_plus_minus'''

def p_unary_expression_not_plus_minus(p):
    '''  unary_expression_not_plus_minus : postfix_expression
             | NOT unary_expression
                                    | cast_expression'''

def p_postfix_expression(p):
    '''  postfix_expression : primary_no_new_array
             | expression_name'''

def p_method_invocation(p):
    '''method_invocation : method_name LPAREN argument_list_optional RPAREN
                                    | primary_no_new_array DOT IDENTIFIER LPAREN argument_list_optional RPAREN'''

def p_argument_list_optional(p):
    '''  argument_list_optional : argument_list
             | empty'''

def p_primary_no_new_array(p):
    '''  primary_no_new_array : literal
             | K_THIS
                                        | LPAREN expression RPAREN
                                        | class_instance_creation_expression
                                        | method_invocation
                                        | array_access'''

def p_class_instance_creation_expression(p):
    'class_instance_creation_expression : K_NEW class_type LPAREN argument_list_optional RPAREN'

def p_argument_list(p):
    '''  argument_list : expression
             | argument_list COMMA expression'''

def p_array_access(p):
    'array_access : expression_name SQUARE_BEGIN expression SQUARE_END'


def p_expression_name(p):
    '''expression_name : IDENTIFIER
                        | ambiguous_name DOT IDENTIFIER'''

def p_method_name(p):
    '''method_name : IDENTIFIER 
                    | ambiguous_name DOT IDENTIFIER'''

def p_ambiguous_name(p):
    '''ambiguous_name : IDENTIFIER 
                        | ambiguous_name DOT IDENTIFIER'''
def p_literal(p):
    '''literal : INT
                | FLOAT
                | CHAR
                | LONG
                | K_NULL'''

# Build the parser
parser = yacc.yacc()

while True :
   try :
       s = raw_input('calc > ')
   except EOFError :
       break
   if not s : continue
   result = parser.parse(s)
   print(result)