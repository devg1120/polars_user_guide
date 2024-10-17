import polars as pl
import numpy as np
import re
import sys
from pygments import highlight
from pygments.lexers import Python3Lexer
from pygments.formatters import TerminalFormatter
from pygments.formatters import Terminal256Formatter
from datetime import datetime
from datetime import date
import numpy as np

BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m' # orange on some systems
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
LIGHT_GRAY = '\033[37m'
DARK_GRAY = '\033[90m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
WHITE = '\033[97m'

RESET = '\033[0m' 

gv = {
      'pl':pl,
      'datetime':datetime,
      'np':np,
     }

def syntx_highlight(code):
    #print(highlight(code, Python3Lexer(), TerminalFormatter()), end="")
    print(highlight(code, Python3Lexer(), Terminal256Formatter()), end="")

def er(title,stmt):
  lv = {'ans' : "not anser"}
  exec(stmt,gv,lv)
  return lv["ans"]

def ep(title,stmt):
  print("---------------------------------------------")
  print(GREEN + title + RESET)
  #print(" " + BLUE + stmt + RESET)
  syntx_highlight(stmt)
  lv = {'ans' : "not anser"}
  exec(stmt,gv,lv)
  print(lv["ans"])


def epn(title,stmt,n):
  print("---------------------------------------------")
  print(GREEN + title + RESET)
  #print(" " + BLUE + stmt + RESET)
  syntx_highlight(stmt)
  lv = {}
  for i in range(n):
      lv['ans' + str(i+1)] = 'not anser'

  exec(stmt,gv,lv)
  for i in range(n):
      if isinstance(lv['ans' + str(i+1)], tuple):
         tup = lv['ans' + str(i+1)]
         print('=== ' + 'ans' + str(i+1) + " " * 3  + RED + tup[0] +RESET) 
         print(tup[1])
      else:
         print('=== ' + 'ans' + str(i+1))
         print(lv['ans' + str(i+1)])
  input(">")


def epna(title,stmt,desc,last,silent):
  ans_list = re.findall('ans[1-9]',stmt)
  n = len(ans_list)
  print("---------------------------------------------")
  print(GREEN + title + RESET + "     " + BRIGHT_YELLOW + desc + RESET)
  if not silent  :
    print(" " + BLUE + stmt + RESET)
    #syntx_highlight(stmt)
  lv = {}
  for i in range(n):
      lv['ans' + str(i+1)] = 'not anser'

  exec(stmt,gv,lv)
  for i in range(n):
      if isinstance(lv['ans' + str(i+1)], tuple):
         tup = lv['ans' + str(i+1)]
         if not silent:
           print(BLUE + '=== ' + title +':  ' +  'ans' + str(i+1) + RESET + " " * 3  + RED + tup[0] +RESET) 
           print(tup[1])
      else:
         if not silent:
           #print(BLUE + '=== ' + 'ans' + str(i+1))
           print(BLUE + '=== ' + title +':  ' +  'ans' + str(i+1) + RESET ) 
           print(lv['ans' + str(i+1)])
  if not silent  :
     if not last :
        input(">")

def vp(title,str):
  print("---------------------------------------------")
  print(GREEN + title + RESET)
  #print(" " + BLUE + str + RESET)
  #print("---------------------------------------------")
  r = re.findall(';',str)
  if len(r) < 1:
     #print(" " + BLUE + str + RESET)
     syntx_highlight(stmt)
     r = eval(str)
     if not r == None:
        print(r)
  else:
    stmts = str.split(';')
    for st in stmts:
        #print(" " + BLUE + st + RESET)
        syntx_highlight(stmt)
        if st == "":
             continue
        r = eval(st)
        print(r)
  input(">")

def vr(title,str):
  print("---------------------------------------------")
  print(GREEN + title + RESET)
  #print(" " + BLUE + str + RESET)
  #print("---------------------------------------------")
  r = re.findall(';',str)
  if len(r) < 1:
     print(" " + BLUE + str + RESET)
     r = eval(str)
     return r 
  else:
    stmts = str.split(';')
    for i, st in enumerate(stmts):
        print(" " + BLUE + st + RESET)
        if st == "":
             continue
        if i == len(stmts) - 1:
           r = eval(st)
           return r
        else:
           eval(st)

###############################################
def main():

    file = "pg.py"
    (l,d) = pg_read(file)
    print(l)
    print(d)


def pg_read(file):
    #file = "pg.py"
    
    prg_list = []
    prg_dict = {}
    desc_dict = {}
    
    #with open(file,encoding='utf-8') as f:
    try:
        f = open(file,encoding='utf-8') 
        lines = f.readlines()
        pgline = False
        comment = False
        pgsource = ""
        name = ""
        desc = ""
        ln = 0
        name_def_ln = 0
        for line in lines:
            ln += 1
            if re.match("<!--",line):
                comment = True 
            elif re.match("-->",line):
                comment = False
            if comment:
                continue
            #print(line.rstrip())
            if re.match("#NAME",line):
                #print("             match #NAME")
                r = re.match(r"^\#NAME\s+(\S+)",line)
                name = r.group(1)
                name_def_ln = ln
                #print(name)
            elif re.match("#DESC",line):
                #print("             match #NAME")
                r = re.match(r"^\#DESC\s+(\S+.*)$",line)
                desc = r.group(1)
                #print(name)
            elif re.match("#START",line):
                #print("             match #START")
                pgline = True
                pgsource = ""
            elif re.match("#END",line):
                #print("             match #END")
                pgline = False
                #print("name", name)
                #print("pgsource",pgsource)
                if name  in prg_dict:
                    print("line:" +str(name_def_ln) + " " + name + " is dupulicated")
                    sys.exit()
                prg_list.append(name)
                prg_dict[name] = pgsource
                desc_dict[name] = desc
            else:
                if pgline:
                    pgsource += line
    except Exception as e:
        print(e)

    return (prg_list, prg_dict, desc_dict)



