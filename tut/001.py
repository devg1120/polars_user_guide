##  template
<!--
#NAME PG
#DESC 
#START
#END
-->

#NAME PG001
#START
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
#END

#NAME PG002 
#DESC Categorical 
#START
pl.enable_string_cache()
cat_series = pl.Series(["Brown", "Panda", "Polar"], dtype=pl.Categorical)
cat_series2 = pl.Series(["Polar", "Panda", "Black"], dtype=pl.Categorical)
ans1 = cat_series == cat_series2
#END

#NAME PG003 
#DESC Enum
#START
pl.enable_string_cache()
dtype = pl.Enum(["Polar", "Panda", "Brown"])
cat_series = pl.Series(["Brown", "Panda", "Polar"], dtype=dtype)
cat_series2 = pl.Series(["Polar", "Panda", "Brown"], dtype=dtype)
ans1 = cat_series == cat_series2
#END

#NAME PG004 
#DESC Data struct
#START
ans1 = pl.Series("a", [1, 2, 3, 4, 5])

df = pl.DataFrame(
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

ans2 = df.head(3)
ans3 = df.tail(3)
ans4 = df.describe()
#END




<!--
#NAME PG
#DESC 
#START
#END
-->
