def remove_whitespace(function):
  new_function = ''
  for i in range(len(function)):
    if function[i] != " ":
      new_function += function[i]
  return new_function

def fix_syntax(function, debug=False):
  function = remove_whitespace(function)
  
  new_function = ""
  is_exponent = False
  is_fraction = False
  
  for i in range(len(function)):
    if debug: print('---')
      
    if function[i] == "/" and is_exponent:
      if debug: print('slash found')
      is_fraction = True

    is_exponent_label = 'E' if is_exponent else ' '
    is_fraction_label = 'F' if is_fraction else ' '
    if debug: print(f'{is_exponent_label}{is_fraction_label} | {function[:i]}[{function[i]}]')
    
    if is_exponent and function[i] == "+":
      if debug: print(f'1: add closing paren after "+" in exp')
      if not is_fraction:
        new_function += '/1'
      is_fraction = False
      new_function += ")"
      is_exponent = False
    elif is_exponent and function[i] == "-" and function[i - 1].isdigit():
      if debug: print(f'2: add closing paren after "#-" in exp')
      if not is_fraction:
        new_function += '/1'
      is_fraction = False
      new_function += ")"
      is_exponent = False

    new_function += function[i]

    if function[i] == "^" and function[i + 1] != "(":
      if debug: print(f'3: add opening paren after "^"')
      new_function += "("
      is_exponent = True

  if is_exponent:
    if debug: print(f'4: add closing paren in exp')
    if not is_fraction:
      new_function += '/1'
    is_fraction = False
    new_function += ")"

  return new_function


def split_terms(function):
  """
  3*x^(2) - 4*x^(-3/4) + 2*x^(-2)

  1. pre-process string, keeping track of +/- OUTSIDE parentheses

  3*x^(2) SPLIT 4*x^(-3/4) SPLIT 2*x^(-2)
  signs: ['+', '-', '+']

  2. split over the string "SPLIT"
  terms: ['3*x^(2)', '4*x^(-3/4)', '2*x^(-2)']
  """

  terms = []
  signs = []
  leading_minus = False

  if function[0] == '-':
    signs += "-"
    function = function[1:]
    leading_minus = True

  plus_split_terms = function.split('+')
  for i in range(len(plus_split_terms)):
    if leading_minus:
      leading_minus = False
    else:
      signs.append("+")

    plus_split_term = plus_split_terms[i].replace('(-', 'PAREN_MINUS')
    minus_split_terms = plus_split_term.split('-')

    terms += minus_split_terms
    for j in range(len(minus_split_terms) - 1):
      signs.append('-')

  for i in range(len(terms)):
    terms[i] = terms[i].replace('PAREN_MINUS', '(-')

  return {'terms': terms, 'signs': signs}


test = split_terms(fix_syntax('-3*x^2 - 4*x^-3/4 + 2*x^2 + 4*x^5/3 - 6/5*x^-2'))
print(test['terms'])
print(test['signs'])
