import re
import sys
print('S\'')
first_line = input()
first_rule, second_rule = re.split('->', first_line)
print('->', first_rule)
print('<br>')
print('->', second_rule)
print('<br>')
for line in sys.stdin :
    ex_rule, new_rule = re.split('->', line)
    ex_rule = ex_rule.strip()
    new_rule = new_rule.strip()
    second_rule = second_rule.replace(ex_rule, new_rule)
    print('->', second_rule)
    print('<br>')

