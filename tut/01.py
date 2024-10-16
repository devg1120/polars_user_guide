import pf as PF
###############################################

dataset = PF.pl.read_csv("../csv/pokemon.csv")


PF.gv["df"] = dataset



PF.epn("001 ",
"""
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
,1)


PG = \
"""
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
PF.epn("002 ",PG,1)

###############################################
