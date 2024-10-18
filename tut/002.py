##  template
<!--
#NAME PG
#DESC 
#START
#END
#TITLE Basic operator
-->

#TITLE Basic operator

#NAME  PG001
#DESC  Try first
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
#END

<!--
https://polars-ja.github.io/docs-ja/user-guide/concepts/lazy-vs-eager/
-->
#NAME  PG002
#DESC  Lazy / eager API
#START
df = pl.read_csv("sample_UTF-8.csv")
ans1 = df
df_small = df.filter(pl.col("age") > 60)
df_agg = df_small.group_by("seibetsu").agg(pl.col("totalmoney").mean())
ans2 = df_agg
#END

#NAME  PG003
#DESC  SCAN collect
#START
q = (
    pl.scan_csv("sample_UTF-8.csv")
    .filter(pl.col("age") > 60)
    .group_by("seibetsu")
    .agg(pl.col("totalmoney").mean())
)

ans1 = q.collect()
#END

#NAME  PG004
#DESC  Streming
#START
q1 = (
    pl.scan_csv("sample_UTF-8.csv")
    .filter(pl.col("age") > 60)
    .group_by("seibetsu")
    .agg(pl.col("totalmoney").mean())
)
ans1 = q1.collect(streaming=True)
#END



<!--
#NAME PG
#DESC 
#START
#END
--EXIT
-->
