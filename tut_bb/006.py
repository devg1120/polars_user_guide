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

#TITLE Aggregation

#GLOBAL_NAME url
#GLOBAL_START
"../csv/legislators-historical.csv"
#GLOBAL_END

#GLOBAL_NAME dtypes
#GLOBAL_START
{
    "first_name": pl.Categorical,
    "gender": pl.Categorical,
    "type": pl.Categorical,
    "state": pl.Categorical,
    "party": pl.Categorical,
}
#GLOBAL_END

#GLOBAL_NAME dataset
#GLOBAL_START
#pl.read_csv("../csv/legislators-historical.csv", dtypes=dtypes).with_columns(
pl.read_csv(url, dtypes=dtypes).with_columns(
             pl.col("birthday").str.to_date(strict=False)
          )
#GLOBAL_END

#NAME  PG001
#DESC  
#START
q = (
    dataset.lazy()
    .group_by("first_name")
    .agg(
        pl.len(),
        pl.col("gender"),
        pl.first("last_name"),
    )
    .sort("len", descending=True)
    .limit(5)
)

df = q.collect()
print(df)
#END



#NAME PG002
#DESC  
#START
q = (
    dataset.lazy()
    .group_by("state", "party")
    .agg(pl.count("party").alias("count"))
    .filter(
        (pl.col("party") == "Anti-Administration")
        | (pl.col("party") == "Pro-Administration")
    )
    .sort("count", descending=True)
    .limit(5)
)

df = q.collect()
print(df)
#END

<!--
#NAME PG003
#DESC 
#START
def compute_age():
    return date.today().year - pl.col("birthday").dt.year()


def avg_birthday(gender: str) -> pl.Expr:
    return (
        compute_age()
        .filter(pl.col("gender") == gender)
        .mean()
        .alias(f"avg {gender} birthday")
    )


q = (
    dataset.lazy()
    .group_by("state")
    .agg(
        avg_birthday("M"),
        avg_birthday("F"),
        (pl.col("gender") == "M").sum().alias("# male"),
        (pl.col("gender") == "F").sum().alias("# female"),
    )
    .limit(5)
)

df = q.collect()
print(df)
#END
-->


#NAME PG004
#DESC 
#START
def get_person() -> pl.Expr:
    return pl.col("first_name") + pl.lit(" ") + pl.col("last_name")


q = (
    dataset.lazy()
    .sort("birthday", descending=True)
    .group_by("state")
    .agg(
        get_person().first().alias("youngest"),
        get_person().last().alias("oldest"),
    )
    .limit(5)
)

df = q.collect()
print(df)
#END

#NAME PG005
#DESC 
#START
def get_person() -> pl.Expr:
    return pl.col("first_name") + pl.lit(" ") + pl.col("last_name")


q = (
    dataset.lazy()
    .sort("birthday", descending=True)
    .group_by("state")
    .agg(
        get_person().first().alias("youngest"),
        get_person().last().alias("oldest"),
        get_person().sort().first().alias("alphabetical_first"),
    )
    .limit(5)
)

df = q.collect()
print(df)
#END


#NAME PG006
#DESC 
#START
def get_person() -> pl.Expr:
    return pl.col("first_name") + pl.lit(" ") + pl.col("last_name")


q = (
    dataset.lazy()
    .sort("birthday", descending=True)
    .group_by("state")
    .agg(
        get_person().first().alias("youngest"),
        get_person().last().alias("oldest"),
        get_person().sort().first().alias("alphabetical_first"),
        pl.col("gender")
        .sort_by(pl.col("first_name").cast(pl.Categorical("lexical")))
        .first(),
    )
    .sort("state")
    .limit(5)
)

df = q.collect()
print(df)
#END


<!--
#NAME PG005
#DESC 
#START
#END
-->
