##  template
<!--
#NAME PG
#DESC 
#START
#END
#TITLE Basic operator
--EXIT
-->

#TITLE Function
#GLOBAL df
#NAME  PG001
#DESC  DataFrame
#START
df = pl.DataFrame(
    {
        "nrs": [1, 2, 3, None, 5],
        "names": ["foo", "ham", "spam", "egg", "spam"],
        "random": np.random.rand(5),
        "groups": ["A", "A", "B", "C", "B"],
    }
)
ans1 = df
#END

#GLOBAL_NAME df
#GLOBAL_START
pl.DataFrame(
    {
        "nrs": [1, 2, 3, None, 5],
        "names": ["foo", "ham", "spam", "egg", "spam"],
        "random": np.random.rand(5),
        "groups": ["A", "A", "B", "C", "B"],
    }
)
#GLOBAL_END

#NAME PG002
#DESC  
#START
df_samename = df.select(pl.col("nrs") + 5)
ans1 = df_samename
#END

#NAME PG003
#DESC Exception
#START
try:
    df_samename2 = df.select(pl.col("nrs") + 5, pl.col("nrs") - 5)
    ans1 = df_samename2
except Exception as e:
    print(e)

#END


#NAME PG004
#DESC 
#START
df_alias = df.select(
    (pl.col("nrs") + 5).alias("nrs + 5"),
    (pl.col("nrs") - 5).alias("nrs - 5"),
)
print(df_alias)
ans1 = df_alias
#END

#NAME PG005
#DESC 
#START
df_alias = df.select(
    pl.col("names").n_unique().alias("unique"),
    pl.approx_n_unique("names").alias("unique_approx"),
)
print(df_alias)
#END


#NAME PG006
#DESC 
#START
df_conditional = df.select(
    pl.col("nrs"),
    pl.when(pl.col("nrs") > 2)
    .then(pl.lit(True))
    .otherwise(pl.lit(False))
    .alias("conditional"),
)
print(df_conditional)
#END

<!--
#NAME PG005
#DESC 
#START
#END
-->
