# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lexer import tokens




def p_compilation_unit(p):
	'compilation_unit :  import_declarations classes_objects'

def p_import_declarations(p):
	'''import_declarations :  import_declaration 
                                            | import_declarations import_declaration'''

def p_import_declaration(p):
	'import_declaration :  import type_name'

def p_classes_objects(p):
	'''classes_objects :  class_object 
                                    | class_object classes_objects'''

def p_class_object(p):
	'''class_object :  class_declaration 
                                | object_declaration 
                                | semi'''

def p_object_declaration(p):
	'object_declaration :  object identifier super BLOCK_BEGIN method_body BLOCK_END'

def p_class_declaration(p):
	'class_declaration :  class identifier class_header super BLOCK_BEGIN class_body_declarations BLOCK_END'

def p_super(p):
	'''super :  K_EXTENDS class_type 
                        | empty'''

def p_class_header(p):
	'class_header :  LPAREN formal_parameter_list RPAREN'

def p_class_body_declarations(p):
	'''class_body_declarations :  class_body_declaration 
                                                    | class_body_declarations class_body_declaration
                                                    | empty'''

def p_class_body_declaration(p):
	'''class_body_declaration :  field_declaration 
                                                | method_declaration'''

def p_formal_parameter_list(p):
	'''formal_parameter_list :  formal_parameter 
                                                | formal_parameter_list COMMA formal_parameter
                                                | empty'''

def p_formal_parameter(p):
	'formal_parameter :  variable_declarator_id COLON type'

def p_class_type(p):
    '''class_type : identifier
                        | K_WITH identifierclass_type'''

def p_field_declaration(p):
	'field_declaration :   val variable_declarator SEMI_COLON'

def p_val(p):
    '''  val : K_VAL
 	   | K_VAR'''

def p_variable_declarator(p):
	'''variable_declarator :  identifier
                                |  identifier COLON type
                                | identifier variable_declarator_extra  '''

def p_variable_declarator_extra(p):
	'''variable_declarator_extra :  ASSIGN variable_initializer
                                        | COLON type ASSIGN variable_initializer'''

def p_variable_initializer(p):
	'''variable_initializer :  expression
                            | array_initializer'''

def p_method_declaration(p):
	'method_declaration :  method_header method_body'

def p_method_header(p):
	'''method_header :  def method_declarator COLON type ASSIGN
                            | def method_declarator ASSIGN '''

def p_method_declarator(p):
	'method_declarator :  identifier LPAREN formal_parameter_list RPAREN'

def p_method_body(p):
	'''method_body :  block 
                                    | semi'''



#BLOCKS AND COMMANDS
#---------------------------------------

def p_block(p):
    '''block : BLOCK_BEGIN block_statements BLOCK_END
                | BLOCK_BEGIN BLOCK_END'''

def p_block_statements(p):
    '''  block_statements : block_statement
 			 | block_statements block_statement'''

def p_block_statement(p):
    '''  block_statement : local_variable_declaration_statement
 			 | statement'''

def p_local_variable_declaration_statement(p):
    'local_variable_declaration_statement : variable_declarators semi'

def p_statement(p):
    '''  statement : statement_without_trailing_substatement
                        | if_then_statement
                        | if_then_else_statement
                        | while_statement
                        | for_statement'''

def p_statement_without_trailing_substatement(p):
    '''  statement_without_trailing_substatement : block
 			 | empty_statement 
                                     | expression_statement 
                                     | switch_statement 
                                     | continue_statement 
                                     | return_statement'''

def p_statement_no_short_if(p):
    '''  statement_no_short_if : statement_without_trailing_substatement
 			 | if_then_else_statement_no_short_if'''

def p_empty_statement(p):
    'empty_statement : semi'

def p_empty(p):
    'empty : '

def p_expression_statement(p):
    'expression_statement : statement_expression semi'

def p_statement_expression(p):
    '''  statement_expression : assignment
 			| method_invocation 
                                    | class_instance_creation_expression'''

def p_if_then_statement(p):
    'if_then_statement : K_IF LPAREN expression RPAREN statement'

def p_if_then_else_statement(p):
    'if_then_else_statement : K_IF LPAREN expression RPAREN statement_no_short_if K_ELSE statement'

def p_if_then_else_statement_no_short_if(p):
    'if_then_else_statement_no_short_if : K_IF LPAREN expression RPAREN statement_no_short_if K_ELSE statement_no_short_if'

def p_switch_statement(p):
    'statement_no_short_if : expression  K_MATCH switch_block'

def p_switch_block(p):
    'switch_block : BLOCK_BEGIN switch_block_statement_groups_optional switch_labels_optional BLOCK_END'

def p_switch_block_statement_groups_optional(p):
    '''  switch_block_statement_groups_optional : switch_block_statement_groups
 			 | empty'''

def p_switch_labels_optional(p):
    '''  switch_labels_optional : switch_labels
 			 | empty'''

def p_switch_block_statement_groups(p):
    '''  switch_block_statement_groups : switch_block_statement_group
 			 | switch_block_statement_groups switch_block_statement_group'''

def p_switch_block_statement_group(p):
    'switch_block_statement_group : switch_labels block_statements'

def p_switch_labels(p):
    '''  switch_labels : switch_label
 			 | switch_labels switch_label'''

def p_switch_label(p):
    '''switch_label : K_CASE expression COLON
                        | K_DEFAULT COLON'''

def p_while_statement(p):
    'while_statement : K_WHILE LPAREN expression RPAREN statement'

def p_for_loop(p):
    'for_loop : K_FOR BLOCK_BEGIN for_exprs for_if_condition BLOCK_END statement'

def p_for_if_condition(p):
    '''for_if_condition : SEMI_COLON if_variables  for_if_condition
                            | if_variables'''

def p_if_variables(p):
    'if_variables : K_IF expression '

def p_for_exprs(p):
    '''for_exprs :  for_variables SEMI_COLON for_exprs
                    | for_variables'''

def p_for_variables(p):
    'for_variables : ID_VARNAME IN expression for_untilTo expression '

def p_for_untilTo(p):
    '''  for_untilTo : K_UNTIL
 		| K_TO'''

def p_statement_expression_list(p):
    '''  statement_expression_list : statement_expression
 			 | statement_expression_list COMMA statement_expression'''

def p_continue_statement(p):
    '''continue_statement : K_CONTINUE IDENTIFIER semi
                                    | K_CONTINUE'''

def p_return_statement(p):
    '''return_statement : K_RETURN expression semi
                                | K_RETURN semi'''




#EXPRESSIONS!
#---------------------------------------
def p_expression(p):
    'expression : assignment_expression'

def p_assignment_expression(p):
    '''  assignment_expression : conditional_expression
 			 | assignment'''

def p_assignment(p):
    'assignment : left_hand_side assignment_operator assignment_expression'

def p_left_hand_side(p):
    '''  left_hand_side : expression_name
 			 | array_access'''

def p_assignment_operator(p):
    'assignment_operator : ASSIGN'

def p_conditional_expression_1(p):
    '''  conditional_expression : conditional_or_expression
 			|  conditional_or_expression  expression COMMA conditional_expression
                                    | expression COLON conditional_expression'''

# def p_conditional_expression_2(p):
#       conditional_expression : conditional_or_expression
#  			 | expression COLON conditional_expression'''

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
                                     | equality_expression NOT_EQUAL relational_expression'''

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
                                    | multiplicative_expression DIV unary_expression
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
                                    | primary_no_new_array DOT identifier LPAREN argument_list_optional RPAREN'''

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
