
#TITLE Windows function

#GLOBAL_NAME df
#GLOBAL_START
pl.read_csv(
            "https://gist.githubusercontent.com/ritchie46/cac6b337ea52281aa23c049250a4ff03/raw/89a957ff3919d90e6ef2d34235e6bf22304f3366/pokemon.csv"
            )
#GLOBAL_END


#NAME  PG001
#DESC  
#START
ans1 = df.head(5)
#END



#NAME PG002
#DESC  
#START
out = df.select(
    "Type 1",
    "Type 2",
    pl.col("Attack").mean().over("Type 1").alias("avg_attack_by_type"),
    pl.col("Defense")
    .mean()
    .over(["Type 1", "Type 2"])
    .alias("avg_defense_by_type_combination"),
    pl.col("Attack").mean().alias("avg_attack"),
)
print(out)
#END

#NAME PG003
#DESC 
#START
filtered = df.filter(pl.col("Type 2") == "Psychic").select(
    "Name",
    "Type 1",
    "Speed",
)
print(filtered)
#END


#NAME PG004
#DESC 
#START
filtered = df.filter(pl.col("Type 2") == "Psychic").select(
    "Name",
    "Type 1",
    "Speed",
)
out = filtered.with_columns(
    pl.col(["Name", "Speed"]).sort_by("Speed", descending=True).over("Type 1"),
)
print(out)
#END

#NAME PG005
#DESC 
#START
out = df.sort("Type 1").select(
    pl.col("Type 1").head(3).over("Type 1", mapping_strategy="explode"),
    pl.col("Name")
    .sort_by(pl.col("Speed"), descending=True)
    .head(3)
    .over("Type 1", mapping_strategy="explode")
    .alias("fastest/group"),
    pl.col("Name")
    .sort_by(pl.col("Attack"), descending=True)
    .head(3)
    .over("Type 1", mapping_strategy="explode")
    .alias("strongest/group"),
    pl.col("Name")
    .sort()
    .head(3)
    .over("Type 1", mapping_strategy="explode")
    .alias("sorted_by_alphabet"),
)
print(out)
#END


#NAME PG006
#DESC  field
#START
df = pl.DataFrame(
    {
        "a": [1, 2, 3],
        "b": [10, 20, 30],
    }
)

out = df.select(
    pl.fold(acc=pl.lit(0), function=lambda acc, x: acc + x, exprs=pl.all()).alias(
        "sum"
    ),
)
print(out)
#END

#NAME PG007
#DESC 
#START
df = pl.DataFrame(
    {
        "a": [1, 2, 3],
        "b": [0, 1, 2],
    }
)

out = df.filter(
    pl.fold(
        acc=pl.lit(True),
        function=lambda acc, x: acc & x,
        exprs=pl.col("*") > 1,
    )
)
print(out)
#END

#NAME PG008
#DESC 
#START
df = pl.DataFrame(
    {
        "a": ["a", "b", "c"],
        "b": [1, 2, 3],
    }
)

out = df.select(pl.concat_str(["a", "b"]))
print(out)
#END
##  template
<!--
#NAME PG
#DESC 
#START
#END
#TITLE Basic operator

#global_name df
#global_start
#global_end
--EXIT
-->
<!--
#NAME PG005
#DESC 
#START
#END
-->
