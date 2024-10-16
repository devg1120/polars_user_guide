import polars as pl
import numpy as np
import re
import sys
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
      if isinstance(lv['ans' + str(i+1)], tuple):
         tup = lv['ans' + str(i+1)]
         print('=== ' + 'ans' + str(i+1) + " " * 30  + RED + tup[0] +RESET) 
         print(tup[1])
      else:
         print('=== ' + 'ans' + str(i+1))
         print(lv['ans' + str(i+1)])

def epn_org(title,stmt,n):
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


# https://polars-ja.github.io/docs-ja/user-guide/expressions/aggregation/
dtypes = {
    "first_name": pl.Categorical,
    "gender": pl.Categorical,
    "type": pl.Categorical,
    "state": pl.Categorical,
    "party": pl.Categorical,
}

dataset = pl.read_csv("csv/legislators-historical.csv", schema_overrides=dtypes).with_columns(
    pl.col("birthday").str.to_date(strict=False)
)

gv["dataset"] = dataset

title= "\"TEST001\""
epn("001 Aggregation",
f"""
q = (
    dataset.lazy()
    .group_by("first_name")
    .agg(
        pl.len(),
        pl.col("gender"),
        pl.first("last_name"),
    )
    .sort("len", descending=True)
    .limit(5)
)
ans1 = {title}, q.collect()

"""
,1)


title= "\"TEST002\""
epn("002 Aggregation",
f"""
q = (
    dataset.lazy()
    .group_by("state")
    .agg(
        (pl.col("party") == "Anti-Administration").sum().alias("anti"),
        (pl.col("party") == "Pro-Administration").sum().alias("pro"),
    )
    .sort("pro", descending=True)
    .limit(5)
)

ans1 = {title}, q.collect()

"""
,1)

title= "\"TEST003\""
epn("003 Aggregation grpup by",
f"""
q = (
    dataset.lazy()
    .group_by("state", "party")
    .agg(pl.count("party").alias("count"))
    .filter(
        (pl.col("party") == "Anti-Administration")
        | (pl.col("party") == "Pro-Administration")
    )
    .sort("count", descending=True)
    .limit(5)
)
ans1 = {title}, q.collect()

"""
,1)

title= "\"TEST004\""
epn("004 Aggregation grpup by",
f"""
q = (
    dataset.lazy()
    .group_by("state")
    .agg(
        (pl.col("party") == "Anti-Administration").sum().alias("anti"),
        (pl.col("party") == "Pro-Administration").sum().alias("pro"),
    )
    .sort("pro", descending=True)
    .limit(5)
)
ans1 = {title}, q.collect()

"""
,1)


def compute_age():
    return date.today().year - pl.col("birthday").dt.year()


def avg_birthday(gender: str) -> pl.Expr:
    return (
        compute_age()
        .filter(pl.col("gender") == gender)
        .mean()
        .alias(f"avg {gender} birthday")
    )

gv["compute_age"] = compute_age
gv["avg_birthday"] = avg_birthday

epn("005 Aggregation grpup by",
"""


q = (
    dataset.lazy()
    .group_by("state")
    .agg(
        avg_birthday("M"),
        avg_birthday("F"),
        (pl.col("gender") == "M").sum().alias("# male"),
        (pl.col("gender") == "F").sum().alias("# female"),
    )
    .limit(5)
)

ans1 = q.collect()

"""
,1)


epn("006 Aggregation grpup by",
"""
def get_person() -> pl.Expr:
    return pl.col("first_name") + pl.lit(" ") + pl.col("last_name")


q = (
    dataset.lazy()
    .sort("birthday", descending=True)
    .group_by("state")
    .agg(
        get_person().first().alias("youngest"),
        get_person().last().alias("oldest"),
    )
    .limit(5)
)

ans1 = q.collect()

"""
,1)

epn("007 Aggregation grpup by",
"""
def get_person() -> pl.Expr:
    return pl.col("first_name") + pl.lit(" ") + pl.col("last_name")


q = (
    dataset.lazy()
    .sort("birthday", descending=True)
    .group_by("state")
    .agg(
        get_person().first().alias("youngest"),
        get_person().last().alias("oldest"),
        get_person().sort().first().alias("alphabetical_first"),
    )
    .limit(5)
)

ans1 = q.collect()

"""
,1)


epn("008 Aggregation grpup by",
"""
def get_person() -> pl.Expr:
    return pl.col("first_name") + pl.lit(" ") + pl.col("last_name")


q = (
    dataset.lazy()
    .sort("birthday", descending=True)
    .group_by("state")
    .agg(
        get_person().first().alias("youngest"),
        get_person().last().alias("oldest"),
        get_person().sort().first().alias("alphabetical_first"),
        pl.col("gender")
        .sort_by(pl.col("first_name").cast(pl.Categorical("lexical")))
        .first(),
    )
    .sort("state")
    .limit(5)
)

ans1 = q.collect()

"""
,1)


