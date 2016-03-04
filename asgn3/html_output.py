def bold(text, bold_part) :
    k = text.rfind(bold_part)
    return text[:k]+'<b>'+bold_part+'</b>'+text[k+len(bold_part):]

def color(text, bold_part) :
    k = text.rfind(bold_part)
    return text[:k]+'<span class="new">'+bold_part+'</span>'+text[k+len(bold_part):]


import re
import sys

header = """<html><head>\n
  <title>Right Sentential form</title>
  <style>
  body { font-family: monospace; font-size:12pt;}
  .new {color: royalblue;}
  </style>
</head>
<body>
"""

footer = """</body></html>"""

print(header)
print(bold('S\'','S\''))
first_line = input()
first_rule, second_rule = re.split('->', first_line)
print(' ->')
print(bold(color(first_rule, first_rule),first_rule))
print('<br>')
second_rule = color(second_rule, second_rule)
for line in sys.stdin :
    ex_rule, new_rule = re.split('->', line)
    temp_rule = ex_rule
    ex_rule = '(.*)'+ ex_rule.strip()+'\\b'
    print(' ->', re.sub(ex_rule, '\\1<b>'+temp_rule+'</b>',second_rule),'<br>')

    second_rule = re.sub(ex_rule,  '\\1'+new_rule, second_rule)
    second_rule = re.sub(r'</?span.*?>','',second_rule)
    second_rule = re.sub(r'</?b>','',second_rule)
    second_rule = color(second_rule, new_rule)
    second_rule = re.sub(r'<empty>','',second_rule)

print(' ->', second_rule)

print(footer)

