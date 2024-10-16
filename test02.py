import polars as pl
import numpy as np
import re
from datetime import datetime

# https://polars-ja.github.io/docs-ja/user-guide/getting-started/

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


def v(title,str):
  print("---------------------------------------------")
  print(GREEN + title + RESET)
  #print(" " + BLUE + str + RESET)
  #print("---------------------------------------------")
  r = re.findall(';',str)
  if len(r) < 1:
     print(" " + BLUE + str + RESET)
     r = eval(str)
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

def v_(title,str):
  print("---------------------------------------------")
  print(GREEN + title + RESET)
  print(" " + BLUE + str + RESET)
  #print("---------------------------------------------")
  r = eval(str)
  print(r)


t = "001"
exp = """
pl.DataFrame(
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

"""
v(t, exp)

t = "002: csv write / read"
exp = """
pl.DataFrame(
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
).write_csv("output.csv");

pl.read_csv("output.csv")
"""
v(t, exp)

df = pl.DataFrame(
    {
        "a": [0,1, 2, 3,4],
        "b": [0.755879,0.070227, 0.026443, 0.329713,0.487679 ],
        "c": [
            datetime(2025, 12, 1),
            datetime(2025, 12, 2),
            datetime(2025, 12, 3),
            datetime(2025, 12, 4),
            datetime(2025, 12, 5),
        ],
        "d": [4.0, 5.0, 6.0,-1,0],
    }
)

t = "003: "
exp = """
pl.DataFrame(
    {
        "a": [0,1, 2, 3,4],
        "b": [0.755879,0.070227, 0.026443, 0.329713,0.487679 ],
        "c": [
            datetime(2025, 12, 1),
            datetime(2025, 12, 2),
            datetime(2025, 12, 3),
            datetime(2025, 12, 4),
            datetime(2025, 12, 5),
        ],
        "d": [4.0, 5.0, 6.0,-1,0],
    }
)

"""
v(t, exp)

v(
"004"
,
 """
df.select(pl.col("a", "b"))

"""
)

v(
"005"
,
"""
df.filter(
    pl.col("c").is_between(datetime(2025, 12, 2), datetime(2025, 12, 3)),
)
"""
)

v(
"006: append column"
,
"""
df.with_columns(pl.col("b").sum().alias("e"), (pl.col("b") + 42).alias("b+42"))
"""
)

df2 = pl.DataFrame(
    {
        "x": range(8),
        "y": ["A", "A", "A", "B", "B", "C", "X", "X"],
    }
)

v(
"007: "
,
"""
df2
"""
)

v("008: ","""
df2.group_by("y", maintain_order=True).len()
""")

v("009: ","""
df2.group_by("y", maintain_order=True).agg(
    pl.col("*").count().alias("count"),
    pl.col("*").sum().alias("sum"),
)
""")

v("010: 組み合わせ","""
df.with_columns((pl.col("a") * pl.col("b")).alias("a * b")).select(
    pl.all().exclude(["c", "d"])
);

df.with_columns((pl.col("a") * pl.col("b")).alias("a * b")).select(
      pl.all().exclude("d")
)

""")

df3 = pl.DataFrame(
    {
        "a": range(8),
        "b": np.random.rand(8),
        "d": [1, 2, 3, 4, 0, -5, -42, None],
    }
)

df4 = pl.DataFrame(
    {
        "x": range(8),
        "y": ["A", "A", "A", "B", "B", "C", "X", "X"],
    }
)

v("011: join","""
df3.join(df4, left_on="a", right_on="x")
""")

v("012: concat","""
df3.hstack(df4)
""")
#########################################
t = ""
exp = """
print("...")
"""
v(t, exp)

