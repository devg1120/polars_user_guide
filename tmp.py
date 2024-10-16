import polars as pl
import numpy as np
import re
import sys
from datetime import datetime
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

RESET = '\033[0m' # called to return to standard terminal text color


gv = {
      'pl':pl,
      'datetime':datetime,
      'np':np,
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

def v_(title,str):
  print("---------------------------------------------")
  print(GREEN + title + RESET)
  print(" " + BLUE + str + RESET)
  #print("---------------------------------------------")
  r = eval(str)
  print(r)

# https://polars-ja.github.io/docs-ja/user-guide/concepts/data-types/categoricals/#enum-vs-categorical
epn("001 Enum vs Categorical",
"""
enum_dtype = pl.Enum(["Polar", "Panda", "Brown"])
enum_series = pl.Series(["Polar", "Panda", "Brown", "Brown", "Polar"], dtype=enum_dtype)
cat_series = pl.Series(
        ["Polar", "Panda", "Brown", "Brown", "Polar"], dtype=pl.Categorical
        )
ans1 = enum_series
ans2 = cat_series
"""
,2)

epn("002 Enum vs Categorical",
"""
cat_series = pl.Series(
        ["Polar", "Panda", "Brown", "Brown", "Polar"], dtype=pl.Categorical
        )
cat2_series = pl.Series(
        ["Panda", "Brown", "Brown", "Polar", "Polar"], dtype=pl.Categorical
        )
ans1 = cat_series.append(cat2_series)

"""
,1)


epn("003 data struct",
"""
ans1 = pl.Series("a", [1, 2, 3, 4, 5])

ans2 = pl.DataFrame(
    {
        "integer": [1, 2, 3, 4, 5],
        "date": [
            datetime(2022, 1, 1),
            datetime(2022, 1, 2),
            datetime(2022, 1, 3),
            datetime(2022, 1, 4),
            datetime(2022, 1, 5),
        ],
        "float": [4.0, 5.0, 6.0, 7.0, 8.0],
    }
)

ans3 = ans2.head(2)
ans4 = ans2.sample(2)


"""
,4)

epn("004 select",
"""
df = pl.DataFrame(
    {
        "nrs": [1, 2, 3, None, 5],
        "names": ["foo", "ham", "spam", "egg", None],
        "random": np.random.rand(5),
        "groups": ["A", "A", "B", "C", "B"],
    }
)

ans1 = df

ans2 = df.select(
    pl.sum("nrs"),
    pl.col("names").sort(),
    pl.col("names").first().alias("first name"),
    (pl.mean("nrs") * 10).alias("10xnrs"),
)

ans3 = df.select(
    pl.col("names").sort(),
)
ans4 = df.sort(
    pl.col("names"),
)

ans5 = df.with_columns(
    pl.sum("nrs").alias("nrs_sum"),
    pl.col("random").count().alias("count"),
)

ans6 = df.filter(pl.col("nrs") > 2)

ans7 = df.group_by("groups").agg(
    pl.sum("nrs"),  # sum nrs by groups
    pl.col("random").count().alias("count"),  # count group members
    # sum random where name != null
    pl.col("random").filter(pl.col("names").is_not_null()).sum().name.suffix("_sum"),
    pl.col("names").reverse().alias("reversed names"),
)
"""
,7)
