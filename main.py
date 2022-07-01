import os
import shutil as sh
import sys
filename = sys.argv[1:][0]
file = open(filename,'r')
instructions = file.read().split('\n')
file.close()
i = 0
cmd_cmdArgSep = '@_'
cmd_ArgSep = ' '
nullArgOp = '0'
safe = False
isFunctionRunning = False
c_argumentsObject = {}
c_funcData = {}
arthOp = '+-*/%<>~^|&!'
indentationMark = '  '
Vars = {}
SuperVars = {'test':0,'version':'pydi-1.func.alpha','auth':'yaver','i':None,'n':None,'PI':22/7}
Scopes = {}
UniversalFuncs = ['str','int','bool','len','complex','type','long','NOT','NEG','float','input','abs']
MathFuncs = ['sin','cos','tan','cot','cosec','sec']
Functions =  {}
math = ''
c_blockIndex = 0
whichFunctionRunning = ''

Errors = [
  'UnknownError',
  'SizeNotDeclaredError',
  'DatabaseNotFoundError',
  'DatabaseCorruptedError',
  'UnsafeToProceed',
  'ValueNotOfGivenTypeError',
  'IllegalTypeError',
  'InvalidExpressionError',
  'InvalidCommandError',
  'SafeModeError',
  'FileNotFoundError',
  'InvalidPython',
  'VaribleNotFound',
  'ArgumentsError',
  'InvalidFunctionalGroupError',
  'InvalidStuctureError',
  'FunctionNotFoundError',
  'MismatchInArgumentsError',
  'NoArgumentsInGlobalError'
]


def Error(index):
  global i,safe
  print('\n\nAt : "'+instructions[i-1]+'"\n',Errors[index],f'\n : at line {i}')
  if safe:
    print ("No Changes Made")
    exit()

NEG = lambda n:n*-1
  

NOT = lambda cond: not eval(parseExpr(str(cond)))

def parseString(string=''):
  string = string.replace('_',' ')
  

def writeFile(args,data):
  f = open(objectifyArgs(args)['f'],'w')
  f.write(str(eval(parseExpr(data.replace('_',' ')))))
  f.close()

def readFile(path):
  if(os.path.exists(path)):
    f = open(path,'r')
    data = f.read()
    f.close()
  else:
    Error(10)
    data = ''
  return data

def addVar(name,value,isGlobal,scope):
  if isGlobal:
    Vars[name] = value
  else:
    if not scope in Scopes:
      Scopes[scope] = {}
    Scopes[scope][name] = value

def createVar(arg,cmdArgs):
  varName = arg.split('=')[0].split(':',1)[1]
  varType = arg.split('=')[0].split(':',1)[0]
  varVal = eval(parseExpr(arg.split('=')[1]))
  isGlobal = True if cmdArgs == '0' else False
  scope = None if isGlobal else objectifyArgs(cmdArgs)['sc']
  try:
    if(varType == 'int'):
      addVar(varName,int(varVal),isGlobal,scope)
    elif(varType == 'str'):
      addVar(varName,varVal.replace('_',' '),isGlobal,scope)
    elif(varType == 'float'):
      addVar(varName,float(varVal),isGlobal,scope)
    elif(varType == 'bool'):
      varVal = False if varVal == 'False' else True
      addVar(varName,varVal,isGlobal,scope)
    else:
      Error(6)
  except:
    Error(5)


def removeSpaces(expr):
  expr = expr.split("'")
  i = 0
  while i < len(expr):
    if (i % 2 == 0): expr[i] = expr[i].replace(' ','')
    else : expr[i] = "'" + expr[i] + "'"
    i += 1
  return ''.join(expr)


def parseExpr(expr):
  err = False
  current_ops = getOperators(expr)
  exprs = removeOperators(expr)
  for i in range(0,len(exprs)):
    if(exprs[i][0] == '$'):
      if(exprs[i][1] == '$'):
        exprs[i] = 'SuperVars["'+exprs[i].replace('$','')+'"]'
      elif isFunctionRunning:
        exprs[i] = 'c_argumentsObject["' + exprs[i][1:] + '"]'
      else:
        err = True
        Error(18)
    elif(exprs[i][0] == "'" and exprs[i][-1] == "'"):
      exprs[i] = exprs[i]
    elif(exprs[i][0].isdecimal()):
      pass
    elif(exprs[i][0] == ':' and ':' != exprs[i][1] and exprs[i].count(':') % 2 == 0):
       func = exprs[i].split(':',2)[1]
       funcExpr = exprs[i].split(':',2)[2]
       exprs[i] = parseFunclExpr(func,funcExpr)
    elif('..' in exprs[i] and '..' != exprs[i][0:2]):
       exprs[i] = exprs[i].split('..') 
       exprs [i] = 'Scopes["' + exprs[i][0] +'"]["' + str(eval(parseExpr(exprs[i][1]))) + '"]'
    elif('.' in exprs[i] and '.' != exprs[i][0]):
      exprs[i] = 'Scopes["' + exprs[i].replace('.','"]["') + '"]'
    elif(exprs[i] == 'False' or exprs[i] == 'True'):
      pass
    elif exprs[i][0] == '{' and exprs[i][-1] == '}':
      exprs[i] = str(Scopes[exprs[i][1:-1]])
    else:
      exprs[i] = 'Vars["'+exprs[i]+'"]'
  expr = ''
  for i in range(0,len(exprs)):
    expr += exprs[i]
    if i<len(current_ops):
      expr += current_ops[i]
  return '""' if err else expr

def parseFunclExpr(func,expr):
  global math
  if(func in UniversalFuncs):
    if(func == 'int' and "'" in expr):
      return f'{func}({parseExpr(expr)}' + '''.replace("'"," "))'''
    return f'{func}({parseExpr(expr)})'
  elif func in MathFuncs:
    if not math: import math
    return f'math.{func}({parseExpr(expr)})'
  else:
    Error(14)

def printOut(arg):
  try:
    print(eval(parseExpr(arg)))
  except KeyError:
    Error(12)
  except Exception as e:
    print(e)
    Error(7)

def getOperators(expr):
  operators = []
  for c in expr:
    if c in arthOp:
      if(c == '|'):
        operators.append(' or ')
      elif(c == '~'):
        operators.append(' == ')
      elif(c == '^'):
        operators.append(' != ')
      elif(c == '&'):
        operators.append(' and ')
      else:
        operators.append(c)
  return operators


def removeOperators(expr):
  for c in arthOp:
    expr = expr.replace(c,',')
  return expr.split(',')


def objectifyArgs(args):
  if(args == '0'):
      return {}
  args = args.split(',')
  args_t = {}
  for j in range(0,len(args)):
      args_t[args[j].split(':')[0]] = args[j].split(':')[1]
  return args_t


class Function(object):
  def __init__(self, args, instrs):
    self.args = args
    self.instrs = instrs

def createDb(name,dbArgs):
  name = eval(parseExpr(name))
  if(os.path.exists(name)):
    sh.rmtree(name)
  os.mkdir(name)
  open(name + '/index.db','w')
  if dbArgs and dbArgs != nullArgOp:
    dbArgs = objectifyArgs(dbArgs)
    if(dbArgs['r'] and dbArgs['c']):
      f = open(name + '/size.native','w')
      f.write(dbArgs['r']+',')
      f.write(dbArgs['c'])
      f.close()

def initDbStruc(path):
  global i
  if os.path.exists(path+'/size.native'):
    f = open(path+'/size.native','r')
    f.close()
    sizes = f.read().split(',')
    r = sizes[0]
    c = sizes[1]
    # Tobe Created
  else:
    Error(1)

def parsePrimitveObject(pre_obj):
  pre_obj = pre_obj[1:-1].split(',')
  obj = {}
  for i in range(0,len(pre_obj)):
    pre_obj[i] = pre_obj[i].split(':')
    obj[pre_obj[i][0]] = eval(parseExpr(pre_obj[i][1]))
  return obj 

def updateObject(arg):
  arg = arg.split('=',1)
  objectName = arg[0]
  objectValue = arg[1]
  if not objectName in Scopes: Scopes[objectName] = {}
  Scopes[objectName] = parsePrimitveObject(objectValue)



def openInDb(db,path):
  global i
  if os.path.exists(db):
    if os.path.exists(db + '/' + path):
      f = open(db + '/' + path,'r')
      return  f
    else:
      Error(3)
  else:
    Error(2)



def parseIntdCommands(instruction):
 if(len(instruction.replace(' ',''))==0):
    return {'cmd':'#','arg':'5','cmdArgs':'0'}
 instruction = instruction[2:]
 cmd = instruction.split(cmd_ArgSep,1)[0]
 arg = removeSpaces(instruction.split(cmd_ArgSep,1)[1])
 if len(cmd.split(cmd_cmdArgSep)) == 2:
    cmdArgs = cmd.split(cmd_cmdArgSep)[1]
    cmd = cmd.split(cmd_cmdArgSep)[0]
 else:
    cmdArgs = '0'
 return {'cmd':cmd,'arg':arg,'cmdArgs':cmdArgs}
 
def updateVar(arg):
  varName = arg.split('=')[0]
  varVal = arg.split('=')[1]
  if '..' in varName and varName[0:2] != '..':
    varName = varName.split('..')
    if not varName[0] in Scopes : Scopes[varName[0]] = {}
    Scopes[varName[0]][eval(parseExpr(varName[1]))] = eval(parseExpr(varVal))
    return
  elif '.' in varName and varName[0] != '.':
    varName = varName.split('.')
    if not varName[0] in Scopes : Scopes[varName[0]] = {}
    Scopes[varName[0]][varName[1]] = eval(parseExpr(varVal))
    return
  addVar(varName,eval(parseExpr(varVal)),True,'')
  

def writeToDb(args,value):
  db = args['db']
  f = openInDb(db,'index.db')
  if(f != None):
    f = f.read()
    if(not f):
      initDbStruc(db)

def read(cmdArgs,arg):
  if 'v' in objectifyArgs(cmdArgs):
    addVar(objectifyArgs(cmdArgs)['v'],readFile(arg),True,'')
  else:
    print(readFile(arg))

def condLoop(arg):
  global i
  cond = parseExpr(arg)
  z = i
  if not eval(cond):
    for j in range(z,len(instructions)):
      if (instructions[j][0:2] != '  ' and len(instructions[j].replace(' ','')) != 0) or len(instructions)-1 == j:
        i = j
        return
  else:
    while(eval(cond)):
      for j in range(z,len(instructions)):
        if instructions[j][0:2] != '  ' and len(instructions[j].replace(' ','')) != 0:
          i = j
          break
        else:
          instr = parseIntdCommands(instructions[j])
          execute(instr['cmd'],instr['cmdArgs'],instr['arg'])
        i = j + 1 if len(instructions) == int(j)+1 else i


def loop(count):
  count = int(eval(parseExpr(count)))
  currentLoopInstr = []
  gi = 0
  SuperVars['n'] = 1
  if isFunctionRunning:
    global c_blockIndex
    c_blockIndex += 1
    print(whichFunctionRunning + '&')
    for j in range(c_blockIndex,len(c_funcData[whichFunctionRunning].instrs)):
      if c_funcData[whichFunctionRunning].instrs[j][2:4] == '  ':
        currentLoopInstr.append(c_funcData[whichFunctionRunning].instrs[j][2:])
        c_blockIndex = j
      else : 
        c_blockIndex = j
        break
  else:
    global i
    while i < len(instructions):
      if instructions[i][0:2] != '  ' and len(instructions[i].replace(' ','')) != 0:
        break
      currentLoopInstr.append(instructions[i])
      i += 1
  for j in range(0,int(count)):
    SuperVars['i'] = gi
    for k in range(0,len(currentLoopInstr)):
      instr = parseIntdCommands(currentLoopInstr[k])
      execute(instr['cmd'],instr['cmdArgs'],instr['arg'])
    gi += 1
    SuperVars['n'] += 1
  SuperVars['i'] = None


def createFunction(arg):
  if ':' in arg:
    name = arg.split(':',1)[0].replace(' ','')
    params = arg.split(':',1)[1].replace(' ','').split(',')
  else:
    name = arg
    params = []
  instrs = []
  global i
  while i < len(instructions):
    if instructions[i][0:2] != '  ' and len(instructions[i].replace(' ','')) != 0: break
    instrs.append(instructions[i])
    i += 1
  Functions[name] = Function(params, instrs)


def call(arg):
  global c_argumentsObject,isFunctionRunning,c_funcData,c_blockIndex,whichFunctionRunning
  if ':' in arg:
    name = arg.split(':',1)[0]
    arguments = arg.split(':',1)[1].split(',')
  else:
    name = arg
    arguments = []
  if not name in Functions:
    Error(16)
    return
  whichFunctionRunning = name
  c_funcData[name] = Functions[name]
  
  if len(c_funcData[name].args) != len(arguments):
    Error(17)
    return
  isFunctionRunning = True
  whichFunctionRunning = name
  c_argumentsObject = 0
  for i in range(0, len(arguments)):
    c_argumentsObject[c_funcData[name].args[i]] = eval(parseExpr(arguments[i]))
  c_blockIndex = 0
  while c_blockIndex < len(c_funcData[name].instrs):
    whichFunctionRunning = name
    instr = parseIntdCommands(c_funcData[name].instrs[c_blockIndex])
    execute(instr['cmd'],instr['cmdArgs'],instr['arg'])
    c_blockIndex += 1
  isFunctionRunning = False
  c_argumentsObject = {}
  c_funcData[name] = {}

def terinary(arg):
  arg = arg.replace(':','?').split('?')
  print(arg)
  cond = eval(parseExpr(removeSpaces(arg[0])))
  toBeExecuted = 1 if cond else 2
  instrs = parseIntdCommands('--'+arg[toBeExecuted])
  print(instrs)
  #execute(instrs[i])

def init_cond_statement(cond):
  pass


def execute(cmd,cmdArgs,arg):
  global safe
  if(cmd == 'createDb'):
    createDb(arg,cmdArgs)
  elif(cmd == 'wDb'):
    writeToDb(objectifyArgs(cmdArgs),arg)
  elif(cmd == 'var'):
    createVar(arg,cmdArgs)
  elif(cmd == 'print'):
    printOut(arg)
  elif(cmd == 'safeMode'):
    safe = False if arg == 'False' else True
  elif(cmd == 'py'):
    try:
      Error(9) if safe else exec(eval(parseExpr(arg)))
    except:
      Error(11)
  elif(cmd == 'read'):
    read(cmdArgs,arg)
  elif(cmd == 'write'):
    writeFile(cmdArgs,arg)
  elif(cmd == 'type'):
    print(type(eval(parseExpr(arg))))
  elif(cmd == 'loop'):
    loop(arg)
  elif(cmd == 'update' or cmd == 'let' or cmd == '$'):
    updateVar(arg)
  elif(cmd == 'while'):
    condLoop(arg)
  elif(cmd == 'printE'):
    print(parseExpr(arg))
  elif(cmd == '#'):
    pass
  elif(cmd == 'BLOCK'):
    createFunction(arg)
  elif(cmd == 'call'):
    call(arg)
  elif(cmd == '::'):
    updateObject(arg)
  elif(cmd == 'if'):
    init_cond_statement(arg)
  elif(cmd == '?'):
    terinary(arg)
  else:
    print(cmd)
    Error(8)

while i < len(instructions):
    #try:
    if len(instructions[i].replace(' ','')) == 0:
      i += 1
      continue
    cmd = instructions[i].split(cmd_ArgSep,1)[0]
    if cmd != '?':
      arg = removeSpaces(instructions[i].split(cmd_ArgSep,1)[1])
    else:
      arg = instructions[i].split(cmd_ArgSep,1)[1]
    if len(cmd.split(cmd_cmdArgSep)) == 2:
      cmdArgs = cmd.split(cmd_cmdArgSep)[1]
      cmd = cmd.split(cmd_cmdArgSep)[0]
    else:
      cmdArgs = '0'
    i += 1
    execute(cmd,cmdArgs,arg)
    #except KeyError:
    #Error(15)
    #i += 1
