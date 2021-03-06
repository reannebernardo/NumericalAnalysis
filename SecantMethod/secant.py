'''
  Program Notes:
    - Does not handle square roots.
    - Reserved letters {e,p,i,c,o,s,n,t,a} *cannot use as variables*
'''

from math import e, pi, sin, cos, tan
import re
from tabulate import tabulate

var = ''
keys = ['e','pi','sin','cos','tan']

def parse(text:str)->list:
  global var
  groupCount=0
  tree = []
  text.replace(' ', '')
  keyStart = []
  keyEnd = []

  # Search text for all occurrence of each key in keys
  # Add its indexes' start and end to hashTab
  for i in keys:
    for j in re.finditer(i, text):
      keyStart.append(j.start())
      keyEnd.append(j.end())

  k = 0
  while k < len(text):
    if k in keyStart:
      if len(tree) != 0 and tree[-1] not in '+-*/^':
        tree.append('*')
      l = keyEnd[keyStart.index(k)]
      tree.append(text[k:l])
      k=l
    
    i = text[k]
    if len(tree) == 0 and i!='-':
      tree.append(i)
    elif i.isdigit():
      if tree[-1].isdigit():
        tree[-1] += i
      else:
        tree.append(i)
    elif i in '+-*/^':
      if i == '-' and (len(tree)==0 or tree[-1] in '+-*/^('):
        tree.append('0')
        tree.append(i)
      else:
        tree.append(i)
    elif i in '()':
      if i == '(':
        if tree[-1].isdigit():
          tree.append('*')
        tree.append(i)
        groupCount += 1
      else:
          if groupCount > 0 and tree[-1] not in '+-*/^':
            tree.append(i)
            groupCount -= 1
          else:
            return 'Error: Invalid groupings'
    elif i.isalpha() and not (k in keyStart):
      if var == '':
        var = i
        if tree[-1].isdigit():
          tree.append('*')
        tree.append(i)
      elif i == var:
        if tree[-1].isdigit():
          tree.append('*')
        tree.append(i)
      else:
        print('Error: Cannot process more than one variable')
    k+=1
  return tree

def infixToPostfix(lst:list)->list:
  stack = []
  output = []
  for i in lst:
    if i in '+-*/^':
      if len(stack) == 0:
        stack.append(i)
      elif stack[-1] == '(':
        stack.append(i)
      elif i == '^':
        stack.append(i)
      elif i in '*/':
        if stack[-1] in '+-':
          stack.append(i)
        else:
          for j in range(len(stack)-1, -1,-1):
            if stack[j] in '*/^':
              output.append(stack.pop())
            else:
              break
          stack.append(i)
      elif i in '+-':
        for j in range(len(stack)-1, -1, -1):
          if stack[j] in '+-*/^':
            output.append(stack.pop())
          else:
            break
        stack.append(i)
    elif i == '(':
      stack.append(i)
    elif i == ')':
      for j in range(len(stack)-1, 0, -1):
        if stack[j] == '(':
          stack.pop()
          break
        else:
          output.append(stack.pop())
    else:
      output.append(i)

  while len(stack) != 0:
    output.append(stack.pop())

  return output

def evalPostfix(pf:list, varVal):
  newpf = pf[:]
  for i in range(len(newpf)):
    if newpf[i].isdigit():
      newpf[i] = float(newpf[i])
    elif newpf[i] == var:
      newpf[i] = varVal
  stack = []
  k = 0
  while k < len(newpf):
    i = newpf[k]
    # Binary Operations
    if str(i) in '+-*/^':
      rightVal = stack.pop()
      leftVal = stack.pop()
      if leftVal == 'e':
        leftVal = e
      elif leftVal == 'pi':
        leftVal = pi
      elif rightVal == 'e':
        rightVal = e
      elif rightVal == 'pi':
        rightVal = pi
      if i == '+':
        stack.append(leftVal + rightVal)
      elif i == '-':
        stack.append(leftVal - rightVal)
      elif i == '*':
        stack.append(leftVal * rightVal)
      elif i == '/':
        stack.append(leftVal / rightVal)
      elif i == '^':
        stack.append(leftVal ** rightVal)
    elif i in ['sin','cos','tan']:
      val = newpf[k+1]
      if i == 'sin':
        stack.append(sin(val))
        k += 1
      elif i == 'cos':
        stack.append(cos(val))
        k += 1
      elif i == 'tan':
        stack.append(tan(val))
        k += 1
    else:
      stack.append(i)
    k+=1
  return stack[0]

def secant(x0, x1, func, iter=1, maxIter=None, maxErr=None):
  if maxIter==None == maxErr==None:
    print('Error: Stopping requirements invalid')
    return
  fnx0 = evalPostfix(func, x0)
  fnx1 = evalPostfix(func, x1)
  if fnx0-fnx1 == 0:
    print('Error: fnx0 is equal to fnx1 resulting in division by zero')
    return
  x2 = x1 - fnx1 * ((x1-x0)/(fnx1-fnx0))
  err = abs(x2-x1)
  yield([iter, x0, x1, fnx0, fnx1, x2, err])
  if maxIter != None:
    if iter == maxIter:
      return
    elif err <= 0:
      print('Program reached 0 error before reaching desired number of iterations')
      return
    else:
      yield from secant(x1, x2, func, iter+1, maxIter, maxErr)
  elif maxErr != None and err <= maxErr:
    return
  else:
    yield from secant(x1, x2, func, iter+1, maxIter, maxErr)

def TryAgain():
  while True:
    x = input('Try Again? [Y] or [N]: ').lower()
    if x == 'y':
      return True
    elif x == 'n':
      return False
    else:
      continue

print('''Root Finding Method: Secant Method
Note:
\tThis program does not handle square roots
\tCharacters 'e,p,i,c,o,s,n,t,a' cannot be used as variables because they are reserved letters used in the program.
Legends:
\tn = number of iterations
\tx0 = first initial point
\tx1 = second initial point
\tCn = approximate root
\tError = Margin of Error
''')

while True:
  try:
    response = ''
  
    fn = input("Enter a function: ")
    x0 = float(input("Enter the first initial point: "))
    x1 = float(input("Enter second initial point: "))

    while True:
      response = int(input("Choose an option for the stopping force: \n[1] Maximum Error \n[2] Maximum Iterations\n"))
      if response == 1:
        maxErr = float(input("Enter the margin of error: "))
        func = infixToPostfix(parse(fn))
        print('\n')
        table = [i for i in secant(x0, x1, func, maxErr=maxErr)]
        print(tabulate(table, headers=["n","x0","x1","f(x0)","f(x1)","Cn","Error"], tablefmt="github"))
        break
      elif response == 2:
        maxIter = int(input("Enter maximum iterations: "))
        func = infixToPostfix(parse(fn))
        print('\n')
        table = [i for i in secant(x0, x1, func, maxIter=maxIter)]
        print(tabulate(table, headers=["n","x0","x1","f(x0)","f(x1)","Cn","Error"], tablefmt="github"))
        break
      else:
        print("Please enter [1] or [2].")
    
    if not TryAgain():
      break

  # except:
  #   input('Error Occurred. Enter anything to exit: ')
  #   break
    
  except IndexError:
    # print('IndexError')
    print("Please enter a function")
  except NameError:
    # print('NameError')
    print("Please enter a valid input.")
  except ValueError:
    # print('ValueError')
    print("Please enter a value.")
  except TypeError:
    # print('TypeError')
    print("Please enter a valid function.")
  except ZeroDivisionError:
    # print('ZeroDivisionError')
    # print('Program tried to divide by zero. Perhaps lessen the number of iterations')
    print("Please enter a valid input")

# Activity 3 A.3
# fn = 'x^6-x-1'
# x0 = 1
# x1 = 1.5
# maxErr = 0.0001
# func = infixToPostfix(parse(fn))
# table = [i for i in secant(x0, x1, func, maxErr=maxErr)]
# print(tabulate(table, headers=["n","x0","x1","f(x0)","f(x1)","Cn","Error"], tablefmt="github"))

# Activity 3 B.3
# fn = 'e^(-x)-x'
# x0 = -1
# x1 = 0
# maxErr = 0.0001
# func = infixToPostfix(parse(fn))

# Test 3
# fn = 'e^(xcos(5))'
# x0 = -1
# x1 = 1
# maxIter = 10
# parsed = parse(fn)
# postfix = infixToPostfix(parsed)
# secant(x0, x1, postfix, maxIter=maxIter)