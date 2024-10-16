import polars as pl
import numpy as np
import re

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

# ランダムなデータを生成
np.random.seed(42)
n = 100

data = {
    "employee_id": np.arange(1, n+1),
    "name": [f"Employee_{i}" for i in range(1, n+1)],
    "age": np.random.randint(22, 65, n),
    "department": np.random.choice(["Sales", "Marketing", "IT", "HR", "Finance"], n),
    "salary": np.random.randint(30000, 150000, n),
    "years_of_service": np.random.randint(0, 30, n),
    "performance_score": np.random.randint(1, 6, n),
    "is_manager": np.random.choice([True, False], n, p=[0.2, 0.8]),
}

# DataFrameの作成
df = pl.DataFrame(data)

# DataFrameの表示
#print(df)

# 基本的な統計情報
#print(df.describe())

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

t = "dataFrame"
exp = """
df;
df.describe()
"""
v(t, exp)

t = "df.select: 列を選ぶ"
v(t, 'df.select("name", "department")')

t = "df.filter: 条件に合う行を抽出する"
v(t,'df.filter("is_manager")')

t = "列名を直接指定しselectで列を選ぶ"
v(t,'df.select("name", "salary", "age", "years_of_service")')


t = "expressionを用いてselectで列を選ぶ"
exp = """
df.select(
    pl.col("name"),
    pl.col("salary"),
    pl.col("age"),
    pl.col("years_of_service"),
)
"""
v(t, exp)

t = "expressionを用いて列の演算を行う"
exp ="""
df.select(
    pl.col("name"),
    pl.col("salary") / 12,
    pl.col("age") - pl.col("years_of_service")
)
"""
v(t, exp)

t = "expressionに別名を与える"
exp = """
df.select(
    pl.col("name"),
    (pl.col("salary") / 12).alias("salary_per_month"),
    (pl.col("age") - pl.col("years_of_service")).alias("age_at_entry")
)
"""
v(t, exp)

t = "集計処理"
exp = """
df.select(
  pl.col("salary").mean().alias("average_of_salary"),
  pl.col("age").min().alias("min_of_age"),
  pl.len().alias("count_of_rows"), 
)
"""
v(t, exp)

t = "df.filter に expression を用いる"
exp = """
df.filter(
    (pl.col("salary") >= 100000) & (pl.col("department") == "IT")
)
"""
v(t, exp)


t = "df.with_columnsの使用例"
exp = """
df;
df.with_columns(
    (pl.col("salary") / 12).alias("salary_per_month"),
    pl.col("years_of_service") + 1,
)
"""
v(t, exp)

t = "df.sort: 列や expression をキーにソートする"
exp = """
df.sort(
    pl.col("name"),
)
"""
v(t, exp)

t = "df.group_by(...).agg(...): DataFrame をグループ化"
exp = """
df.group_by("department").agg(
    pl.len().alias("num_of_employees"),
    pl.col("is_manager").sum().alias("num_of_managers"),
    pl.sum("salary").alias("amount_of_salary"),
    pl.mean("age").alias("mean_of_age")
)

"""
v(t, exp)
#########################################
t = ""
exp = """
print("...")
"""
v(t, exp)

