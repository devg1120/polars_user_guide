import polars as pl
import numpy as np
import re
import sys
import copy
from pygments import highlight
from pygments.lexers import Python3Lexer
from pygments.formatters import TerminalFormatter
from pygments.formatters import Terminal256Formatter
from datetime import datetime
from datetime import date
from datetime import timedelta
import numpy as np
#import seaborn as sns

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

def display(t,s):
    print(GREEN)
    print(t)
    print(YELLOW)
    print(s)
    print(RESET)

class Config:


    is_short_ans = False

    def __init__(self):
        self.is_short_ans = False

    def set_short_ans(self, v):
        self.is_short_ans = v

    def short_ans(self):
        #return self.short_ans
        return  self.is_short_ans
        #return False
        #return True


#short_ans = True

config = Config()

gv = {
      'pl':pl,
      'datetime':datetime,
      'date':date,
      'timedelta':timedelta,
      'np':np,
      #'sns':sns,
      'display':display,
      'config': copy.deepcopy(config),
      #'config': Config(),
     }


def syntx_highlight(code):
    #print(highlight(code, Python3Lexer(), TerminalFormatter(colorscheme="xcode",linenos=True,full=True)), end="")
    #print(highlight(code, Python3Lexer(), TerminalFormatter(bg="light",linenos=True,full=True)), end="")
    #print(highlight(code, Python3Lexem(), TerminalTrueColorFormatter(bg="light",linenos=True,full=True)), end="")
    print(highlight(code, Python3Lexer(), Terminal256Formatter()), end="")

def er(title,stmt):
  lv = {'ans' : "not anser"}
  exec(stmt,gv,lv)
  return lv["ans"]

def keyword(str):
    r = re.sub('(def)', YELLOW +  '\\1' + RESET, str)  
    r = re.sub('(if)' , YELLOW +  '\\1' + RESET, r)  
    r = re.sub('(for)', YELLOW +  '\\1' + RESET, r)  
    r = re.sub('(try)', YELLOW +  '\\1' + RESET, r)  
    r = re.sub('(except)', YELLOW +  '\\1' + RESET, r)  
    #r = re.sub('([=,.])', YELLOW +  '\\1' + RESET, r)  
    return r

def string(str):
    r = re.sub('(\".*?\")',RED +  '\\1' + RESET, str)  # "--"
    r = re.sub('(\'.*?\')',RED +  '\\1' + RESET, r)   # '--'
    r = re.sub('([\(\)])',CYAN +  '\\1' + RESET, r)   # ( )
    r = re.sub('([\{\}])',CYAN +  '\\1' + RESET, r)   # { }
    return keyword(r)

def comment(str):
    m = re.match("^(.*)(\#.*)$",str)     
    if m != None:
        return m.group(1)  +  BLUE + m.group(2) + RESET

    else:
        #return GREEN + str + RESET
        return string(str)

def color(str):
    return comment(str)

def source_print(stmt):
    stmt_list = stmt.split("\n")
    cnt = 0
    for line in stmt_list:
        cnt += 1
        print(str(cnt).zfill(2),end=" ")
        #print(BLUE + line + RESET , end="\n")
        print(color(line) , end="\n")

def ep(title,stmt):
  print("---------------------------------------------")
  print(GREEN + title + RESET)
  print(" " + BLUE + stmt + RESET)
  #syntx_highlight(stmt)
  #source_print(stmt)
  lv = {'ans' : "not anser"}
  exec(stmt,gv,lv)
  print(lv["ans"])


def epn(title,stmt,n):
  print("---------------------------------------------")
  print(GREEN + title + RESET)
  print(" " + BLUE + stmt + RESET)
  #syntx_highlight(stmt)
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


def epna(title,stmt,desc,last,silent, source):
  ans_list = re.findall('ans[1-9]',stmt)
  n = len(ans_list)
  print("---------------------------------------------")
  print(GREEN + title + RESET + "     " + BRIGHT_YELLOW + desc + RESET)
  if not silent  :
    #print(" " + BLUE + stmt + RESET)
    #syntx_highlight(stmt)
    source_print(stmt)
  if source:
      return

  lv = {}
  for i in range(n):
      lv['ans' + str(i+1)] = 'not anser'
      gv['config'] = copy.deepcopy(config)
  try:
     exec(stmt,gv,lv)
     for i in range(n):
         if isinstance(lv['ans' + str(i+1)], tuple):
            tup = lv['ans' + str(i+1)]
            if not silent:
              print(BLUE + '=== ' + title +':  ' +  'ans' + str(i+1) + RESET + " " * 3  + RED + tup[0] +RESET) 
              print(tup[1])
         else:
            if not silent:
              #if short_ans:
              #print("config.short_ans:",config.short_ans())
              #if config.short_ans():
              if gv["config"].short_ans():
                #print(BLUE + '=== ' + 'ans' + str(i+1))
                print(RED + '*=== ' + title +':  ' +  'ans' + str(i+1) + RESET , end = " ") 
                print(lv['ans' + str(i+1)])
              else:
                #print(BLUE + '=== ' + 'ans' + str(i+1))
                print(BLUE + '=== ' + title +':  ' +  'ans' + str(i+1) + RESET, end = " " ) 
                print(lv['ans' + str(i+1)])
  except Exception as e:
      print(RED + "Exception" + RESET)
      print(e)
  if not silent  :
     print(GREEN + title + RESET + " END")
  if not silent  :
     if not last :
        key = input(">")
        #key = input(GREEN + title + RESET + ">")
        if key == 'q':
            sys.exit()

def epna_t(title,stmt,desc):
  ans_list = re.findall('ans[1-9]',stmt)
  n = len(ans_list)
  print("---------------------------------------------")
  print( title  + "     " +  desc )
  print(" " + stmt )
  #syntx_highlight(stmt)
  lv = {}
  for i in range(n):
      lv['ans' + str(i+1)] = 'not anser'
  try:
     exec(stmt,gv,lv)
     for i in range(n):
         if isinstance(lv['ans' + str(i+1)], tuple):
            tup = lv['ans' + str(i+1)]
            print( '=== ' + title +':  ' +  'ans' + str(i+1)  + " " * 3  + tup[0] ) 
            print(tup[1])
         else:
            print( '=== ' + title +':  ' +  'ans' + str(i+1)  ) 
            print(lv['ans' + str(i+1)])
  except Exception as e:
      print(RED + "Exception" + RESET)
      print(e)

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
    
    title = ""
    prg_list = []
    prg_dict = {}
    desc_dict = {}

    global_v = False
    global_name = "df"
    global_source = """
pl.DataFrame(
    {
        "nrs": [1, 2, 3, None, 5],
        "names": ["foo", "ham", "spam", "egg", "spam"],
        "random": np.random.rand(5),
        "groups": ["A", "A", "B", "C", "B"],
    }
)
"""
    global_name = ""
    global_source = ""
    #gv[global_name] = eval(global_source)

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
            if re.match("-EXIT",line):
               break
            if re.match("--EXIT",line):
               break
            #print(line.rstrip())
            if re.match("#NAME",line):
                #print("             match #NAME")
                r = re.match(r"^\#NAME\s+(\S+)",line)
                try:
                  name = r.group(1)
                  name_def_ln = ln
                except Exception as e:
                  name_def_ln = ln
                  print(RED + "line:" + str(ln) + " name not define" + RESET)
                  sys.exit()
                #print(name)
            elif re.match("#DESC",line):
                #print("             match #NAME")
                r = re.match(r"^\#DESC\s+(\S+.*)$",line)
                try:
                   desc = r.group(1)
                except Exception as e:
                   desc = ""
                #print(name)
            elif re.match("#TITLE",line):
                r = re.match(r"^\#TITLE\s+(\S+.*)$",line)
                try:
                   title = r.group(1)
                except Exception as e:
                   title = ""
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
                desc = ""
            elif re.match("#GLOBAL_NAME",line):
                r = re.match(r"^\#GLOBAL_NAME\s+(\S+.*)$",line)
                try:
                   global_name = r.group(1)
                   print("set global: " + global_name);
                except Exception as e:
                    pass
            elif re.match("#GLOBAL_START",line):
                global_v = True
                global_source = ""
            elif re.match("#GLOBAL_END",line):
                global_v = False
                gv[global_name] = eval(global_source, gv)
                #print("set global: " + global_name);
            else:
                if pgline:
                    pgsource += line
                elif global_v:
                    global_source += line
    except Exception as e:
        print(e)

    return (title,prg_list, prg_dict, desc_dict)



