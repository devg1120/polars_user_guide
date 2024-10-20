<!--
https://qiita.com/nkay/items/9cfb2776156dc7e054c8

-->

#TITLE pandasから移行する人向け polars使用ガイド


#GLOBAL_NAME df
#GLOBAL_START
pl.DataFrame(
    {
        "Integer": [1, 2, 3, 4],
        "Float": np.array([1, 2, 3, 4], dtype=float),
        "Datetime": [datetime(2022, 4, 1)] * 4,
        "String": ["test", "train", "test", "train"],
    }
)
#GLOBAL_END


#NAME PG001
#DESC 基礎
#START

# データ型

ans1  = pl.Int8
ans2  = pl.Int64
ans3  = pl.UInt8
ans4  = pl.UInt64
ans5  = pl.Float32
ans6  = pl.Float64	
ans7  = pl.Boolean
ans8  = pl.String
ans9  = pl.Categorical
ans10 = pl.Enum	
ans11 = pl.List
ans12 = pl.Array
ans13 = pl.Struct
ans14 = pl.Date
ans15 = pl.Time
ans16 = pl.Datetime
ans17 = pl.Duration
ans18 = pl.Object

config.set_short_ans(True)
#END

#NAME PG002
#DESC ファイル読み書き
#START

# ファイル読み込み

df = pl.read_csv("./pokemon.csv")
ans1 = df

df.write_csv("./example.csv")

#tf = open("./tmp.txt","w")
#print(df.glimpse(), file=tf)

ans2 = df.glimpse(return_as_string=True)
ans3 = df.describe()

#END

#NAME PG003
#DESC 選択
#START
# []を使った行の選択
ans1 = df[0]
ans2 = df[1:3]
# []を使った行の選択
rng = np.random.default_rng(5)
df_num = pl.DataFrame(rng.integers(0, 10, (6, 3)), schema="ABC")

ans1 = df_num
ans2 = df_num.filter(pl.col("A") > 5)
ans3 = df_num.filter((pl.col("A") < pl.col("B")) & (pl.col("C") < 5))
ans4 = df_num.filter(
    pl.col("A") < pl.col("B"),
    pl.col("C") < 5,
)

ans5 = df_num.filter(B=2)
ans6 = df_num.filter(pl.col("A") < 1, B=2, C=3)
ans7 = df_num.filter([False, True, False, True, True, False])

#END

#NAME PG004
#DESC 行操作
#START
# リストに含まれるかどうかを判定するSeries.is_in()

ans1 = df.get_column("Integer").is_in([2, 4, 6])

ans2 = df.filter(pl.col("Integer").is_in([2, 4, 6]))

#END

#NAME PG005
#DESC ユニーク行・重複行
#START
# ユニーク行・重複行

rng = np.random.default_rng(0)
df_dup = pl.DataFrame(
    {
        "a": ["one", "one", "two", "two", "two", "three", "four"],
        "b": ["x", "y", "x", "y", "x", "x", "x"],
        "c": rng.random(7),
    }
)

ans1 = df_dup.unique(subset=["a", "b"])

ans2 = df_dup.unique(subset=["a"])

ans3 = df_dup.unique(subset=["a"], keep="last")

ans4 = df_dup.unique(subset=["a"], keep="none")

ans5 = df_dup.is_duplicated()

ans6 = df_dup.get_column("a").is_duplicated()


#END

#NAME PG006
#DESC 列操作
#START
# .get_column()を使ったシリーズの選択
ans1 = df.get_column("Integer")

# .get_columns()を使ったシリーズの選択
ans2 = type(df.get_columns())
ans3 = df.get_columns()[1]

ans4 = df.get_column_index("Float")

# .select()を使った列選択
ans5 = df.select("Integer")
ans6 = df.select("Integer", "Float") 
ans7 = df.select(pl.col("Integer"), pl.col("Float"))
ans8 = df.select(pl.col("Integer")*2, pl.col("Float").sum())

#END

#NAME PG007
#DESC 列操作
#START
# 列の追加

# 新しいシリーズの作成を伴う操作
new_seires = (df.get_column("Integer") * 2).alias("Integer2")
ans1 = df.with_columns(new_seires)

# エクスプレッションによる操作
new_column = (pl.col("Integer") * 2).alias("Integer2")
ans2 = df.with_columns(new_column)

# 既存の列名と同名の列を追加すると、追加ではなく更新になります。
ans3 = df.with_columns(pl.col("Integer") * 100)

# .with_columns()にエクスプレッションを複数渡すと、一度に複数の列を追加できます。
ans4 = df.with_columns(
    pl.sum("Integer").alias("Integer2"), (pl.col("Float") * 100).alias("Arange")
)

# 新しい列名をキーワード引数として指定することもできます。
ans5 = df.with_columns(
    Integer2=pl.sum("Integer"),
    Arange=pl.col("Float") * 100
)

ans6 = df.with_row_count()

# .select()でも列の追加は可能です。
ans7 = df.select(pl.arange(0, df.height).alias("index"), pl.all())


#END

#NAME PG008
#DESC 四則演算
#START
# 四則演算

rng = np.random.default_rng(0)
df_num = pl.DataFrame(rng.integers(0, 10, (6, 3)), schema="ABC")

ans1 = df_num

ans2 = df_num + 2
ans3 = df_num * 2
ans4 = df_num.get_column("A") ** 2
ans5 = df_num.select(pl.all().pow(2))
ans6 = df_num + df_num.get_column("B")
ans7 = df_num.get_column("A") + df_num.get_column("B")


#END

#NAME PG009
#DESC 比較演算
#START
# 比較演算

rng = np.random.default_rng(0)
df_num = pl.DataFrame(rng.integers(0, 10, (6, 3)), schema="ABC")

ans1 = df_num

ans2 = df_num.get_column("A") == 0

ans3 = df_num.get_column("A") > 2

ans4 = df_num.get_column("A") > df_num.get_column("B")

ans5 = pl.Series(["foo", "bar", "baz"]) == pl.Series(["foo", "bar", "qux"])

#END

#NAME PG010
#DESC 集合関数
#START
# 集合関数
rng = np.random.default_rng(0)
df_num = pl.DataFrame(rng.integers(0, 10, (6, 3)), schema="ABC")

ans1 = df_num

ans2 = df_num.sum()
ans3 = df_num.mean()
ans4 = df_num.quantile(0.5)
ans5 = df_num.fold(lambda a, b: a+b)

# 現回数を集計する.value_counts()
ans6 = df_num["A"].value_counts()
ans7 = df_num["A"].value_counts(sort=True)
ans8 = df_num.select(pl.col("A").value_counts())

#END

#NAME PG011
#DESC 列操作：エクスプレッションの主な使い方

#START
# 列選択・指定：pl.col()

df = pl.DataFrame(
    {
        "Integer": [1, 2, 3, 4],
        "Float": np.array([1, 2, 3, 4], dtype=float),
        "Datetime": [datetime(2022, 4, 1)] * 4,
        "String": ["test", "train", "test", "train"],
    }
)

ans1 = df.select(pl.col("String"))
ans2 = df.select(pl.col("String", "Integer"))

# 列名　正規表現
ans3 = df.select(pl.col(r"^[DS].+$"))

ans4 = df.select(pl.col(pl.Int64))
ans5 = df.select(pl.col("*"))
ans6 = df.select(pl.exclude("Integer"))
ans7 = df.select(pl.col("Integer").alias("ABC"), pl.col("Integer").alias("DEF"))

#END 


#NAME PG012
#DESC ソート
#START
# ソート・並び替え
df = df_unsort = pl.DataFrame(
    {
        "col1": ["A", "A", "B", None, "D", "C"],
        "col2": [2, 1, 9, 8, 7, 4],
        "col3": [0, 1, 9, 4, 2, 3],
        "col4": ["a", "B", "c", "D", "e", "F"],
    }
)
ans1 = df

ans2 = df.select(pl.col("*").sort_by("col1"))
ans3 = df.select(pl.col("*").sort_by("col1",descending=True))

tmp = df.select(pl.col("*").sort_by("col2"))
ans4 = tmp.select(pl.col("*").sort_by("col1"))
ans5 = tmp.select(pl.col("*").sort_by("col1", nulls_last=True))

#END

#NAME PG013
#DESC 集合計算
#START
ans1 = df.select(pl.col("Integer").sum())
ans2 = df.select(pl.sum("Integer"))

pl.Config.set_tbl_cols(-1)
ans3 = df.select(
    pl.count("Integer").alias("count"),
    pl.n_unique("Integer").alias("n_unique"),
    pl.max("Integer").alias("max"),
    pl.min("Integer").alias("min"),
    pl.mean("Integer").alias("mean"),
    pl.median("Integer").alias("median"),
    pl.quantile("Integer", 0.5).alias("50%tile"),
    pl.std("Integer").alias("std"),
    pl.var("Integer").alias("var"),
)

#END

#NAME PG014
#DESC  OVER
#START

# over
ans1 = df
ans2 = df.select(pl.col("Integer", "Float").sum().over("String"))

pass
#END

#NAME PG015
#DESC 条件分岐：when()
#START

# 条件分岐：when()

ans1 = df.select(
    pl.when(pl.col("Integer") > 2).then(pl.lit("big")).otherwise(pl.lit("small"))
)

ans2 = df.select(
    pl.when(pl.col("Integer") > 2)
    .then(pl.col("String").str.to_uppercase())
    .otherwise(pl.col("String").str.replace_all(r".", "x"))
)

ans3 = df.select(
    pl.when(pl.col("Integer") == 1)
    .then(pl.lit("one"))
    .when(pl.col("Integer") == 2)
    .then(pl.lit("two"))
    .when(pl.col("Integer") == 3)
    .then(pl.lit("three"))
    .otherwise(pl.lit("other"))
)

new_column = pl.coalesce(
    pl.when(pl.col("Integer") == 1).then(pl.lit("one")).otherwise(None),
    pl.when(pl.col("Integer") == 2).then(pl.lit("two")).otherwise(None),
    pl.when(pl.col("Integer") == 3).then(pl.lit("three")).otherwise(pl.lit("other")),
)
ans4 = df.select(new_column)

ans5 = df.select(pl.col("Float").where(pl.col("Integer") > 2))

#END

#NAME PG016
#DESC 複数のデータフレームの結合・マージ
#START

# pl.concat()による結合（スタック・連結）

df1 = pl.DataFrame(
    {"A": ["A0", "A1"], "B": ["B0", "B1"], "C": ["C0", "C1"], "D": ["D0", "D1"]}
)
df2 = pl.DataFrame(
    {"A": ["A2", "A3"], "B": ["B2", "B3"], "C": ["C2", "C3"], "D": ["D2", "D3"]}
)
df3 = pl.DataFrame(
    {"A": ["A4", "A5"], "B": ["B4", "B5"], "C": ["C4", "C5"], "D": ["D4", "D5"]}
)

ans1 = pl.concat([df1, df2, df3])

df1 = pl.DataFrame(
    {"A": ["A0", "A1"], "B": ["B0", "B1"], "C": ["C0", "C1"]}
)
df2 = pl.DataFrame(
    {"A": ["A2", "A3"], "B": ["B2", "B3"], "D": ["D2", "D3"]}
)
df3 = pl.DataFrame(
    {"A": ["A4", "A5"], "B": ["B4", "B5"], "C": ["C4", "C5"], "D": ["D4", "D5"]}
)

ans2 = pl.concat([df1, df2, df3], how="diagonal")

df1 = pl.DataFrame({"A": ["A0", "A1", "A2"], "B": ["B0", "B1", "B2"]})
df2 = pl.DataFrame({"C": ["C0", "C1"], "D": ["D0", "D1"]})

ans3 = pl.concat([df1, df2], how="horizontal")



pass
#END

#NAME PG017
#DESC 複数のデータフレームの結合・マージ
#START

# DataFrame.join()による結合（マージ）

left = pl.DataFrame(
    {
        "key1": ["K0", "K0", "K1", "K2"],
        "key2": ["K0", "K1", "K0", "K1"],
        "A": ["A0", "A1", "A2", "A3"],
        "B": ["B0", "B1", "B2", "B3"],
    }
)
right = pl.DataFrame(
    {
        "key1": ["K0", "K1", "K1", "K2"],
        "key2": ["K0", "K0", "K0", "K0"],
        "C": ["C0", "C1", "C2", "C3"],
        "D": ["D0", "D1", "D2", "D3"],
    }
)

ans1 = "left", left.join(right, on=["key1", "key2"], how="left")
ans2 = "right",left.join(right, on=["key1", "key2"], how="right")
ans3 = "full", left.join(right, on=["key1", "key2"], how="full")
ans4 = "full", left.join(right, on=["key1", "key2"], how="full", coalesce=True)
#ans5 = "cross",left.join(right, on=["key1", "key2"], how="cross")
ans6 = "semi", left.join(right, on=["key1", "key2"], how="semi")
ans7 = "anti", left.join(right, on=["key1", "key2"], how="anti")

#END

#NAME PG018
#DESC Group By
#START1

# Group_by

rng = np.random.default_rng(0)
df = pl.DataFrame(
    {
        "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
        "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
        "C": rng.random(8),
        "D": rng.random(8),
    }
)

ans1 = df.group_by("A", "B").sum()
ans2 = df.group_by("A", pl.col("B").str.to_uppercase().alias("BIG_B")).first()

dfna = pl.DataFrame(
    [[np.nan, 2, 3], [1, None, 4], [2, 1, 3], [1, 2, 2]], schema="ABCD"
)

ans3 = dfna

ans4 = dfna.group_by("A").sum()
ans5 = dfna.group_by("B").sum()


#END

#NAME PG019
#DESC  group_by
#START

rng = np.random.default_rng(0)
df = pl.DataFrame(
    {
        "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
        "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
        "C": rng.random(8),
        "D": rng.random(8),
    }
)
grouped = df.group_by("A")
ans1 = type(grouped)

#for group_name, group_df in grouped:
#    print(f"{group_name = }")
#    print(group_df)
#    print("---")

ans2 =  grouped.all()

tmp = ""
for group_name, group_df in grouped:
    tmp += group_name[0]
    tmp += str(group_df)
    tmp += "\n---\n"

ans3 = tmp

#END

#NAME PG020
#DESC  集計 ピボットテーブル
#START
rng = np.random.default_rng(0)
df = pl.DataFrame(
    {
        "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
        "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
        "C": rng.random(8),
        "D": rng.random(8),
    }
)

ans1 = df.group_by("A", "B").head()

ans2 = df.group_by("A", "B").len()

ans3 = df.group_by("A", "B").agg(
    pl.sum("*").name.suffix("_sum"),
    pl.mean("C").name.suffix("_mean"),
    pl.std("D").name.suffix("_std"),
)

# ピボットテーブル
pivot_table = df.pivot(on="B", index="A", values="C", aggregate_function="sum")
ans4 = "pivot", pivot_table 

#END

#NAME PG021
#DESC 損値・欠損データの扱い
#START
df_missing = pl.DataFrame(
    {"A": [1, 2, None, 4, None, None], "B": [np.nan, 4, 3, 2, np.nan, None]}
)

ans1 = df_missing

ans2 = df_missing.with_columns(
    A_is_null=pl.col("A").is_null(),
    B_is_null=pl.col("B").is_null(),
    B_is_nan=pl.col("B").is_nan(),
)

ans3 = df_missing.null_count()

ans4 = df_missing.select(
    pl.all().count().name.suffix("_count"),
    pl.all().len().name.suffix("_len"),
)

# 欠損値の伝搬

ans5 = df_missing.with_columns(
    A_plus_B=pl.col("A") + pl.col("B"),  # 加算演算によるAとBの和
    sum_A_B=pl.sum_horizontal("A", "B"),  # 集計関数によるAとBの和
)

ans6 = df_missing.with_columns(
    gt=(pl.col("A") > pl.col("B")),
    eq=(pl.col("A") == pl.col("B")),
)

#END

#NAME PG022
#DESC 損値・欠損データの扱い
#START
df_missing = pl.DataFrame(
    {"A": [1, 2, None, 4, None, None], "B": [np.nan, 4, 3, 2, np.nan, None]}
)

# 欠損値の穴埋め

ans1 = df_missing.fill_null(99)

ans2 = df_missing.fill_nan(99)

ans3 = df_missing.fill_null(pl.Series([11, 12, 13, 14, 15, 16]))

ans4 = df_missing.fill_nan(pl.col("A"))

ans5 = df_missing.fill_null(strategy="mean")

#END

#NAME PG023
#DESC テキストデータを扱う
#START

df_str = pl.DataFrame(
    {"orig": ["A", "B", "Aaba", "Baca", None, "CABA", "dog", "cat"]}
)

ans1 = df_str.with_columns(
    # シリーズの操作
    df_str.get_column("orig").str.len_bytes().alias("len"),
    df_str.get_column("orig").str.to_lowercase().alias("lower"),
    # エクスプレッションの操作
    pl.col("orig").str.to_uppercase().alias("upper"),
    pl.col("orig").str.slice(1, 3).alias("slice"),
)

ans2 = df_str.select(pl.col("orig") + "_" + pl.col("orig"))


df_str2 = pl.DataFrame({"a": ["Tokyo", "東京", "Cafe", "Café", "Café", None]}).with_columns(
    pl.col("a").str.len_bytes().alias("len_bytes"),
    pl.col("a").str.len_chars().alias("len_chars"),
)

ans3 = df_str2

#END

#NAME PG024
#DESC テキストデータを扱う
#START
# 正規表現検索で一致部分を抽出
ans1 = pl.Series(["a1a2", "b1", "c1"]).str.extract(r"([ab])?(\d)")
ans2 = pl.Series(["a1a2", "b1", "c1"]).str.extract(r"([ab])?(\d)", group_index=2)

# 特定の文字列を含むかどうかを検索
ans3 = pl.Series(["1", "2", "3a", "3b", "03c", "4dx"]).str.contains(r"[0-9][a-z]")

df_str = pl.DataFrame(
    {"orig": ["A", "B", "Aaba", "Baca", None, "CABA", "dog", "cat"]}
)
# 正規表現による文字列の置換
ans4 = df_str["orig"].str.replace(r"^.a|dog", "XX-XX ")

#END

#NAME PG025
#DESC 時系列データを扱う
#START

ans1 = pl.date_range(
    datetime(2022, 1, 1),
    datetime(2022, 1, 10),
    "1d",
    eager=True,
)

ans2 = pl.datetime_range(
    datetime(2022, 1, 1),
    datetime(2022, 1, 10),
    timedelta(days=1, hours=12),
    eager=True,
)

# 文字列から時系列に変換する.str.strptime()
df_drange = pl.DataFrame(
    {
        "drange_str": [
            "2022-01-01 00:00:00",
            "2022-01-02 12:00:00",
            "2022-01-04 00:00:00",
            "2022-01-05 12:00:00",
            "2022-01-07 00:00:00",
            "2022-01-08 12:00:00",
            "2022-01-10 00:00:00",
        ]
    }
)

ans3 = df_drange.get_column("drange_str").dtype
# String

ans4 = df_drange.get_column("drange_str").str.strptime(pl.Datetime).dtype
# Datetime(time_unit='us', time_zone=None)

new_column = pl.col("drange_str").str.strptime(pl.Datetime).alias("drange")
ans5 = df_drange.with_columns(new_column)


#END

<!--
#NAME PG000
#DESC 
#START
pass
#END



#TITLE

#GLOBAL_NAME
#GLOBAL_START
#GLOBAL_END

#NAME PG001
#DESC 
#START
#END
-EXIT
-->
