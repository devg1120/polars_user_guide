##  template
<!--
#NAME PG
#DESC 
#START
#END
#TITLE Basic operator
--EXIT
-->

#TITLE Casting

#NAME  PG001
#DESC  DataFrame
#START
df = pl.DataFrame(
    {
        "integers": [1, 2, 3, 4, 5],
        "big_integers": [1, 10000002, 3, 10000004, 10000005],
        "floats": [4.0, 5.0, 6.0, 7.0, 8.0],
        "floats_with_decimal": [4.532, 5.5, 6.5, 7.5, 8.5],
    }
)
print(df)
#END


#GLOBAL_NAME df
#GLOBAL_START
pl.DataFrame(
    {
        "integers": [1, 2, 3, 4, 5],
        "big_integers": [1, 10000002, 3, 10000004, 10000005],
        "floats": [4.0, 5.0, 6.0, 7.0, 8.0],
        "floats_with_decimal": [4.532, 5.5, 6.5, 7.5, 8.5],
    }
)

#GLOBAL_END

#NAME PG002
#DESC  
#START
out = df.select(
    pl.col("integers").cast(pl.Float32).alias("integers_as_floats"),
    pl.col("floats").cast(pl.Int32).alias("floats_as_integers"),
    pl.col("floats_with_decimal")
    .cast(pl.Int32)
    .alias("floats_with_decimal_as_integers"),
)
print(out)
#END


#NAME PG003
#DESC 
#START
out = df.select(
    pl.col("integers").cast(pl.Int16).alias("integers_smallfootprint"),
    pl.col("floats").cast(pl.Float32).alias("floats_smallfootprint"),
)
print(out)
#END


#NAME PG004
#DESC 
#START
try:
    out = df.select(pl.col("big_integers").cast(pl.Int8))
    print(out)
except Exception as e:
    print(e)
#END

#NAME PG005
#DESC 
#START
out = df.select(pl.col("big_integers").cast(pl.Int8, strict=False))
print(out)
#END


#NAME PG006
#DESC 
#START
df2 = pl.DataFrame({"strings_not_float": ["4.0", "not_a_number", "6.0", "7.0", "8.0"]})
try:
    out = df2.select(pl.col("strings_not_float").cast(pl.Float64))
    print(out)
except Exception as e:
    print(e)
#END

#NAME PG007
#DESC 
#START
df = pl.DataFrame(
    {
        "integers": [-1, 0, 2, 3, 4],
        "floats": [0.0, 1.0, 2.0, 3.0, 4.0],
        "bools": [True, False, True, False, True],
    }
)

out = df.select(pl.col("integers").cast(pl.Boolean), pl.col("floats").cast(pl.Boolean))
print(out)
#END

#NAME PG008
#DESC  datetime
#START
df = pl.DataFrame(
    {
        "date": pl.date_range(date(2022, 1, 1), date(2022, 1, 5), eager=True),
        "datetime": pl.datetime_range(
            datetime(2022, 1, 1), datetime(2022, 1, 5), eager=True
        ),
    }
)

out = df.select(pl.col("date").cast(pl.Int64), pl.col("datetime").cast(pl.Int64))
print(out)
#END


#NAME PG009
#DESC 
#START
df = pl.DataFrame(
    {
        "date": pl.date_range(date(2022, 1, 1), date(2022, 1, 5), eager=True),
        "string": [
            "2022-01-01",
            "2022-01-02",
            "2022-01-03",
            "2022-01-04",
            "2022-01-05",
        ],
    }
)

out = df.select(
    pl.col("date").dt.to_string("%Y-%m-%d"),
    pl.col("string").str.to_datetime("%Y-%m-%d"),
)
print(out)
#END


<!--
#NAME PG005
#DESC 
#START
#END
-->
