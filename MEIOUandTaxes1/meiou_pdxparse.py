import os
import glob
os.chdir(os.path.dirname(__file__))

nl = '\n'
tb = '\t'

def pairwise(list): # returns elements from list in pairs
   if len(list) % 2 == 1:
      raise ValueError('List must be even')
   i = 0
   while i < len(list):
      yield (list[i], list[i+1])
      i += 2

def parseline(line: str):
   tokens: list[str] = []
   comment = ''
   quoted = False
   brackets = 0
   token = ''
   for i, char in enumerate(line):
      if char == '"':
         token += char
         quoted = not quoted
         if not quoted:
            tokens.append(token)
            token = ''
      elif quoted:
         token += char
      elif char == '#':
         if token:
            tokens.append(token)
         comment = line[i:]
         break
      elif char in ' \t':
         if not token:
            continue
         tokens.append(token)
         token = ''
      else:
         token += char
   if token:
      tokens.append(token)
   return tokens, comment

def parse(file, filename):
   indents = []
   previndents = 0
   output = ''
   comment = ''
   for lnum, line in enumerate(file):
      line = line.rstrip('\n')
      previndents = len(indents)
      for i, ind in enumerate(indents): #track indents
         if line.startswith(ind):
            line = line[len(ind):]
         else:
            indents = indents[:i]
            break
      else: #new indent?
         l = line.lstrip()
         if (num := len(line) - len(l)):
            indents.append(line[:num])
            line = l
      
      if len(indents) < previndents: # dedent
         for x in range(previndents - len(indents)):
            output += f'\n{tb * (previndents - x - 1)}}}'
      elif len(indents) > previndents: #indent
         output += ' = {'
      if comment:
         output += f'  {comment}'
      output += f'\n{tb * len(indents)}'
      #line contents
      
      tokens, comment = parseline(line)
      for i, token in enumerate(tokens):
         if token.startswith('{') and token.endswith('}'):
            out = eval(token[1:-1])
            if type(out) in (float, int):
               if out > (2**31-1)/1000:
                  raise ValueError(f"Calculated value above maximum: file '{filename}', line {lnum+1}")
               if out < -(2**31)/1000:
                  raise ValueError(f"Calculated value below minimum: file '{filename}', line {lnum+1}")
               tokens[i] = f'{out:.3f}'
            else:
               tokens[i] = str(out)
      if len(tokens) == 1:
         output += tokens[0]
      elif len(tokens) % 2 == 1:
         output += f"{tokens[0]} = {{ {' '.join(map(' = '.join, pairwise(tokens[1:])))} }}"
      else:
         output += ' '.join(map(' = '.join, pairwise(tokens)))

   for x in range(previndents):
      output += f'\n{tb * (previndents - x - 1)}}}'
   output += '\n'
   return output[1:]

try:
   with open('meiou.pdx', 'r') as f:
      parsed = parse(f, 'meiou.pdx')
   with open('meiou.txt', 'w') as o:
      o.write(parsed)
except Exception as e:
   print("Exception found! Cancelled parsing.\n")
   print(e)
   input("Press enter to exit...")
