##  template
<!--
#NAME PG
#DESC 
#START
#END
-->
<!--
https://polars-ja.github.io/docs-ja/user-guide/concepts/contexts/
-->

<!--
┌─────┬───────────────────────┬─────────┬────────┬───┬─────────┬───────┬────────────┬───────────┐
│ #   ┆ Name                  ┆ Type 1  ┆ Type 2 ┆ … ┆ Sp. Def ┆ Speed ┆ Generation ┆ Legendary │
│ --- ┆ ---                   ┆ ---     ┆ ---    ┆   ┆ ---     ┆ ---   ┆ ---        ┆ ---       │
│ i64 ┆ str                   ┆ str     ┆ str    ┆   ┆ i64     ┆ i64   ┆ i64        ┆ bool      │
╞═════╪═══════════════════════╪═════════╪════════╪═══╪═════════╪═══════╪════════════╪═══════════╡
│ 1   ┆ Bulbasaur             ┆ Grass   ┆ Poison ┆ … ┆ 65      ┆ 45    ┆ 1          ┆ false     │
│ 2   ┆ Ivysaur               ┆ Grass   ┆ Poison ┆ … ┆ 80      ┆ 60    ┆ 1          ┆ false     │
│ 3   ┆ Venusaur              ┆ Grass   ┆ Poison ┆ … ┆ 100     ┆ 80    ┆ 1          ┆ false     │
│ 3   ┆ VenusaurMega Venusaur ┆ Grass   ┆ Poison ┆ … ┆ 120     ┆ 80    ┆ 1          ┆ false     │
│ 4   ┆ Charmander            ┆ Fire    ┆ null   ┆ … ┆ 50      ┆ 65    ┆ 1          ┆ false     │

-->

#GLOBAL_NAME df
#GLOBAL_START
pl.read_csv(
            "../csv/pokemon.csv"
            )
#GLOBAL_END

#TITLE  BASIC & CONTEXT

#NAME PG000
#START
ans1 = df
ans2 = df.columns
ans3 = df.head(1)
#END

#NAME PG000-1
#DESC pl.Config.set_tbl_cols(-1)
#START
pl.Config.set_tbl_cols(-1)
#pl.Config.set_tbl_rows(-1)
ans1 = df
ans2 = df.columns
ans3 = df.head(1)
#END

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
#ans3 = df.tail(3)
#ans4 = df.describe()
#END

#NAME PG005
#DESC  context
#START
df = pl.DataFrame(
    {
        "nrs": [1, 2, 3, None, 5],
        "names": ["foo", "ham", "spam", "egg", None],
        "random": np.random.rand(5),
        "groups": ["A", "A", "B", "C", "B"],
    }
)
ans1 = df
ans2 = "select", df.select(
    pl.sum("nrs"),
    pl.col("names").sort(),
    pl.col("names").first().alias("first name"),
    (pl.mean("nrs") * 10).alias("10xnrs"),
)
#END

#NAME PG006
#DESC  context
#START
df = pl.DataFrame(
    {
        "nrs": [1, 2, 3, None, 5],
        "names": ["foo", "ham", "spam", "egg", None],
        "random": np.random.rand(5),
        "groups": ["A", "A", "B", "C", "B"],
    }
)
ans1 = df
ans2 = "with_columns", df.with_columns(
    pl.sum("nrs").alias("nrs_sum"),
    pl.col("random").count().alias("count"),
 )
#END

#NAME PG007
#DESC  filter
#START
df = pl.DataFrame(
    {
        "nrs": [1, 2, 3, None, 5],
        "names": ["foo", "ham", "spam", "egg", None],
        "random": np.random.rand(5),
        "groups": ["A", "A", "B", "C", "B"],
    }
)
ans1 = df

ans2 = "filter", df.filter(pl.col("nrs") > 2)

#END

#NAME PG008
#DESC  group_by
#START
df = pl.DataFrame(
    {
        "nrs": [1, 2, 3, None, 5],
        "names": ["foo", "ham", "spam", "egg", None],
        "random": np.random.rand(5),
        "groups": ["A", "A", "B", "C", "B"],
    }
)
ans1 = df

ans2 = "group_by", df.group_by("groups").agg(
    pl.sum("nrs"),  # sum nrs by groups
    pl.col("random").count().alias("count"),  # count group members
    # sum random where name != null
    pl.col("random").filter(pl.col("names").is_not_null()).sum().name.suffix("_sum"),
    pl.col("names").reverse().alias("reversed names"),
)
#END


#NAME PG009
#DESC 
#START
for name, data in df.group_by("Type 1"):  
    print(name)
    print(data)
#END

#NAME PG010
#DESC 
#START
ans1 = df.partition_by("Type 1")  
#END


<!--
#NAME PG
#DESC 
#START
#END
-->
