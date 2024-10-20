import sys
import re
import pf as PF
###############################################

def  main():
   args = sys.argv

   pgv_list = []

   if len(args) < 2:
       for gv in globals():
           if re.match("PG[0-9]+",gv):
               pgv_list.append(gv)
           #else:
           #    print(gv)
   else:
       num = args[1]
       gv = "PG" + num.zfill(3)
       pgv_list.append(gv)

   #print(pgv_list)
   #sys.exit()

   dataset = PF.pl.read_csv("../csv/pokemon.csv")
   PF.gv["df"] = dataset

   for test_case in pgv_list:
      if test_case in globals():
          print("exist")
      else:
          print("not exist")
          continue

      PG = eval(test_case)
      PF.epna(test_case,PG)
   

PG001 =\
"""
ans1 = "OK PG001", df.select(
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


PG002 = \
"""
ans1 = "OK PG002", df.select(
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


PG003 = \
"""
ans1 = "OK PG003", df.select(
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

### PT4

PG004 = \
"""
ans1 = "OK PG004", df.select(
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

###############################################
###############################################

if __name__ == "__main__":
    main()
