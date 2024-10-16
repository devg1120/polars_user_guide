import polars as pl
import numpy as np
import re
import sys
from datetime import datetime

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

RESET = '\033[0m' # called to return to standard terminal text color


gv = {
      'pl':pl,
      'datetime':datetime,
     }

def er(title,stmt):
  lv = {'ans' : "not anser"}
  exec(stmt,gv,lv)
  return lv["ans"]

def ep(title,stmt):
  print("---------------------------------------------")
  print(GREEN + title + RESET)
  print(" " + BLUE + stmt + RESET)
  lv = {'ans' : "not anser"}
  exec(stmt,gv,lv)
  print(lv["ans"])
  input(">")

def _epn(title,stmt,n):
    pass

def epn(title,stmt,n):
  print("---------------------------------------------")
  print(GREEN + title + RESET)
  print(" " + BLUE + stmt + RESET)
  lv = {}
  for i in range(n):
      lv['ans' + str(i+1)] = 'not anser'

  exec(stmt,gv,lv)
  for i in range(n):
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
     print(" " + BLUE + str + RESET)
     r = eval(str)
     if not r == None:
        print(r)
  else:
    stmts = str.split(';')
    for st in stmts:
        print(" " + BLUE + st + RESET)
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
  input(">")

def v_(title,str):
  print("---------------------------------------------")
  print(GREEN + title + RESET)
  print(" " + BLUE + str + RESET)
  #print("---------------------------------------------")
  r = eval(str)
  print(r)


epn("001",
"""
df = pl.DataFrame(
    {
        "integer": [1, 2, 3],
        "date": [
            datetime(2025, 1, 1),
            datetime(2025, 1, 2),
            datetime(2025, 1, 3),
        ],
        "float": [4.0, 5.0, 6.0],
        "string": ["a", "b", "c"],
    }
)
ans1 = type(df)
ans2 = df
"""
,2)

epn("002 index",
"""
df = pl.DataFrame(
    {
        "integer": [1, 2, 3],
        "date": [
            datetime(2025, 1, 1),
            datetime(2025, 1, 2),
            datetime(2025, 1, 3),
        ],
        "float": [4.0, 5.0, 6.0],
        "string": ["a", "b", "c"],
    }
)
ans1 = type(df['string'])
ans2 = df['string']
"""
,2)

epn("003 index index",
"""
df = pl.DataFrame(
    {
        "integer": [1, 2, 3],
        "date": [
            datetime(2025, 1, 1),
            datetime(2025, 1, 2),
            datetime(2025, 1, 3),
        ],
        "float": [4.0, 5.0, 6.0],
        "string": ["a", "b", "c"],
    }
)
ans1 = type(df['string'][2])
ans2 = df['string'][2]
"""
,2)

ep("004 csv read",
"""
df = pl.read_csv("output.csv")

ans = df

"""
)

ep("005 csv read",
"""
df = pl.read_csv("./csv/sample_UTF-8.csv")

ans = df

"""
)

_epn("006 csv read",
"""
df = pl.read_csv("./csv/sample_UTF-8.csv")

name_list = df['name']

ans2 = len(name_list)
str = ""
for name in name_list:
       str += name
       str += " "
ans1 = str
"""
,2)

epn("007 slice",
"""
df = pl.read_csv("./csv/sample_UTF-8.csv")

ans1 = df[1]
ans2 = df[1:5]

"""
,2)


ep("008 is_in",
"""
df = pl.read_csv("./csv/sample_UTF-8.csv")

ans = df.get_column("name").is_in(["コソユワイ"])

"""
)

ep("009 filter",
"""
df = pl.read_csv("./csv/sample_UTF-8.csv")
ans = df.filter(pl.col("age") < 22)
"""
)

epn("009 filter",
"""
df = pl.read_csv("./csv/sample_UTF-8.csv")

ans1 = df.filter(pl.col("age") > 62, pl.col("totalmoney") > 98000, )

ans2 = df.filter(pl.col("age") > 62, pl.col("totalmoney") > 98000, pl.col("seibetsu") == "men")

ans3 = df.filter(pl.col("age") > 62, pl.col("totalmoney") > 98000, pl.col("seibetsu") == "women")

ans4 = df.filter(pl.col("name").str.contains("カナヨ"))

ans5 = df.filter(pl.col("userid").str.contains(r"^[A-F]"))

ans5 = df.filter(pl.col("userid").str.contains(r"[1-3]$")).head(5)
d = df.filter(pl.col("userid").str.contains(r"[1-3]$")).head(5)

ans6 = ""
for  e in d["name"]:
    ans6 +=  e +";"

"""
,6)

ep("010 select where",
"""
df = pl.read_csv("./csv/sample_UTF-8.csv")
ans = df.select(pl.col("name","age").where(pl.col("age") < 22))
"""
)




