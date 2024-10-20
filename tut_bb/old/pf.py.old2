import polars as pl
import numpy as np
import re
import sys
from pygments import highlight
from pygments.lexers import Python3Lexer
from pygments.formatters import TerminalFormatter
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
    #print(highlight(code[1:-1], Python3Lexer(), TerminalFormatter()), end="")
    print(highlight(code, Python3Lexer(), TerminalFormatter()), end="")

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
from pygments import highlight
from pygments.lexers import Python3Lexer
from pygments.formatters import HtmlFormatter
from pygments.formatters import Terminal256Formatter
from pygments.formatters import TerminalFormatter

# https://pygments.org/docs/formatters/

#code = 'print("Hello World")'

code = """
ans1 = "OK", df.select(
    "Type 1",
    "Type 2",
    pl.col("Attack").mean().over("Type 1").alias("avg_attack_by_type"),
    pl.col("Defense")
    .mean()
    .over(["Type 1", "Type 2"])
    .alias("avg_defense_by_type_combination"),
    pl.col("Attack").mean().alias("avg_attack"),
)
"""
#print(highlight(code, Python3Lexer(), HtmlFormatter()))
#print(highlight(code, Python3Lexer(), Terminal256Formatter()))
print(highlight(code, Python3Lexer(), TerminalFormatter()))
