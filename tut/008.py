
#TITLE  List and Array

#GLOBAL_NAME df
#GLOBAL_START
pl.read_csv(
            "https://gist.githubusercontent.com/ritchie46/cac6b337ea52281aa23c049250a4ff03/raw/89a957ff3919d90e6ef2d34235e6bf22304f3366/pokemon.csv"
            )
#GLOBAL_END

#GLOBAL_NAME weather
#GLOBAL_START
pl.DataFrame(
    {
        "station": ["Station " + str(x) for x in range(1, 6)],
        "temperatures": [
            "20 5 5 E1 7 13 19 9 6 20",
            "18 8 16 11 23 E2 8 E2 E2 E2 90 70 40",
            "19 24 E9 16 6 12 10 22",
            "E2 E0 15 7 8 10 E1 24 17 13 6",
            "14 8 E0 16 22 24 E1",
        ],
    }
)
#GLOBAL_END

#NAME  PG001
#DESC  
#START
ans1 = weather
#END

#NAME  PG002
#DESC  
#START
ans1 = weather.with_columns(pl.col("temperatures").str.split(" "))

#END

#NAME  PG003
#DESC  
#START
ans1  = weather.with_columns(pl.col("temperatures").str.split(" ")).explode(
    "temperatures"
)
#END

#NAME  PG004
#DESC  
#START
ans1 = weather.with_columns(pl.col("temperatures").str.split(" ")).with_columns(
    pl.col("temperatures").list.head(3).alias("top3"),
    pl.col("temperatures").list.slice(-3, 3).alias("bottom_3"),
    pl.col("temperatures").list.len().alias("obs"),
)
#END

#NAME PG005
#DESC 
#START
ans1 = weather.with_columns(
    pl.col("temperatures")
    .str.split(" ")
    .list.eval(pl.element().cast(pl.Int64, strict=False).is_null())
    .list.sum()
    .alias("errors")
)
#END

#NAME PG006
#DESC 
#START
ans1 = weather.with_columns(
    pl.col("temperatures")
    .str.split(" ")
    .list.eval(pl.element().str.contains("(?i)[a-z]"))
    .list.sum()
    .alias("errors")
)
#END



#NAME PG007
#DESC 
#START
weather_by_day = pl.DataFrame(
    {
        "station": ["Station " + str(x) for x in range(1, 11)],
        "day_1": [17, 11, 8, 22, 9, 21, 20, 8, 8, 17],
        "day_2": [15, 11, 10, 8, 7, 14, 18, 21, 15, 13],
        "day_3": [16, 15, 24, 24, 8, 23, 19, 23, 16, 10],
    }
)
ans1 = weather_by_day

rank_pct = (pl.element().rank(descending=True) / pl.col("*").count()).round(2)

ans2 = weather_by_day.with_columns(
    # create the list of homogeneous data
    pl.concat_list(pl.all().exclude("station")).alias("all_temps")
).select(
    # select all columns except the intermediate list
    pl.all().exclude("all_temps"),
    # compute the rank by calling `list.eval`
    pl.col("all_temps").list.eval(rank_pct, parallel=True).alias("temps_rank"),
)
#END

#NAME PG008
#DESC 
#START
array_df = pl.DataFrame(
    [
        pl.Series("Array_1", [[1, 3], [2, 5]]),
        pl.Series("Array_2", [[1, 7, 3], [8, 1, 0]]),
    ],
    schema={
        "Array_1": pl.Array(pl.Int64, 2),
        "Array_2": pl.Array(pl.Int64, 3),
    },
)
ans1 = array_df

ans2 = array_df.select(
    pl.col("Array_1").arr.min().name.suffix("_min"),
    pl.col("Array_2").arr.sum().name.suffix("_sum"),
)

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
