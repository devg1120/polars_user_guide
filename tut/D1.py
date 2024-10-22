
https://datasciencemore.com/category/ds-lecture/polars/
#TITLE  polars講座

<!--
#DESC SV生成
#df = sns.load_dataset("diamonds")
#df.head(30).to_csv('./csv/sns_diamonds.csv')
-->

#GLOBAL_NAME df1
#GLOBAL_START
pl.read_csv("./csv/sns_diamonds.csv")
#GLOBAL_END

#GLOBAL_NAME df2
#GLOBAL_START
pl.read_csv("./csv/sns_iris.csv")
#GLOBAL_END

#NAME PG001
#DESC csv-file load
#START
ans1 = df1
#END

https://datasciencemore.com/polars-filter/
#NAME PG002
#DESC filter：行の抽出
#START
ans1 = df1.filter(pl.col("price") == 337)
ans2 = df1.filter(pl.col("depth") >= 62)
ans3 = df1.filter(pl.col("carat").is_between(0.23, 0.27))
ans4 = df1.filter(pl.col("color") == "E")
ans5 = df1.filter(pl.col("color") != "E")
ans6 = df1.filter(pl.col("color").cast(pl.Utf8).is_in(["I", "J"]))
ans7 = df1.filter((pl.col("depth") >= 22) & (pl.col("color") == "H"))
ans8 = df1.filter((pl.col("depth") >= 22) | (pl.col("color") == "H"))

# (depth列が62以上かつcolor列がH)ではない行を抽出（NOT）
ans9 = df1.filter(~((pl.col("depth") >= 22) & (pl.col("color") == "H")))
# 変数
x = 337
ans10 = df1.filter(pl.col("price") == x)

#END

https://datasciencemore.com/polars-select/
#NAME PG003
#DESC select：列の抽出
#START
#df = sns.load_dataset("iris")
#df.head(30).to_csv('./sns_iris.csv')
ans1 = df2

# sepal_length列, species列を抽出
ans2 = df2.select("sepal_length", "species")

# sepal_length列をシリーズ（ベクトル）として抽出
ans3 = df2.get_column("sepal_length")

# sepalが含まれる列名を抽出 
ans4 = df2.select("^*sepal.*$")

# float型の列を抽出する 
ans5 = df2.select(pl.col(pl.Float64))

#END

https://datasciencemore.com/polars-with_columns/
#NAME PG004
#DESC with_columns：列の追加・更新
#START
ans1 = df1.select("depth", "table", "color")
ans2 = df1.with_columns(
    color = pl.lit("color"),
    new_1 = pl.lit(1),
    new_2 = pl.lit(2)
)

ans3 = df1.with_columns(
    new = pl.col("depth") * 2
)

ans4 = df1.with_columns(
    new = pl.col("color") + "OK"
)

ans5 = df1.with_columns(
    new =
    pl.when(pl.col("color") == "E")
    .then(pl.lit("isE"))
    .otherwise(pl.lit("notE"))
    )

ans6 = df1.with_columns(
    new =
    pl.when(pl.col("color") == "E")
    .then(pl.lit("E"))
    .when(pl.col("color") == "I")
    .then(pl.lit("I"))
    .otherwise(pl.lit("not_E_I"))
)



#END

https://datasciencemore.com/polars-join/
#NAME PG005
#DESC join：キー結合
#START
 # キー結合
 # inner_join
 # left_join
 # right_join
 # outer_join

# データフレームの表示行数を指定
pl.Config.set_tbl_rows(6)

# 名前のデータフレーム定義
df_name = pl.DataFrame(
    {
        "key":[1, 1, 3, 2, 5],
        "name":["asuka", "yuuki", "siho", "rina", "manaka"]
     }
     )
 
# 所属のデータフレーム定義
df_group = pl.DataFrame(
    {
        "key":[1, 2, 3, 4],
        "group":["nogi", "sakura", "hinata", "yosimoto"]
     }
     )

# inner_join
ans1 = "inner_join",df_name.join(df_group, on="key", how="inner")
ans2 = "inner_join",df_name.join(df_group, on="key")

# left_join

ans3 = "left_join",df_name.join(df_group, on="key", how="left")

# right_join

# polarsはright_joinできないので、dfを入れ替える。
ans4 = df_group.join(df_name, on="key", how="left")

# outer_join

ans5 = "outer_join",df_name.join(df_group, on="key", how="outer")

#END

https://datasciencemore.com/polars-concat/
#NAME PG006
#DESC concat：縦横結合
#START

pl.Config.set_tbl_rows(6)

# 名前のデータフレーム 1
df_name_1 = pl.DataFrame(
    {
        "key":[1, 2],
        "name":["asuka", "rina"]
     }
     )

# 名前のデータフレーム 2
df_name_2 = pl.DataFrame(
    {
        "key":[1, 2, 3],
        "name":["hinako", "yui", "kyouko"]
     }
     )

# グループのデータフレーム
df_group = pl.DataFrame(
    {
        "group":["nogi", "sakura", "nogi", "sakura", "hinata"]
     }
     )

# 縦横結合

df_name = pl.concat([df_name_1, df_name_2])
ans1 = df_name

# 横結合

df_name_group = pl.concat([df_name, df_group], how="horizontal")
ans2 = df_name_group

#END

https://datasciencemore.com/polars-groupby/
#NAME PG007
#DESC groupby：グルーピング
#START
pl.Config.set_tbl_rows(6)

df = pl.DataFrame(
  {
    "class":["a", "b", "c", "c", "a", "c", "b", "a", "c", "b", "a"],
    "gender":["M", "F", "F", "M", "F", "M", "M", "F", "M", "M", "F"],
    "height":[162, 150, 168, 173, 162, 198, 182, 154, 175, 160, 172]
  }
  )

# classでグルーピングしてheightの平均を算出
ans1 = df.group_by("class").mean()

# classでグルーピングしてheightの平均を算出（classでソート）
ans2 = df.group_by("class").mean().sort("class")

# 集約メソッド

# classでグルーピングしてheightの最大値を算出
ans3 = df.group_by("class").max().sort("class")

# class, genderでグルーピングしてheightの平均を算出
ans4 = df.group_by(["class", "gender"]).mean().sort(["class", "gender"])

#END


https://datasciencemore.com/polars-sort/
#NAME PG008
#DESC sort：ソート
#START

pl.Config.set_tbl_rows(5)
 
# データ読み込み
df = pl.read_csv("./csv/sns_diamonds.csv")
ans1 = df


ans2 = df.sort("depth", descending=False)

ans3 = df.sort(["depth", "table"])
#END


https://datasciencemore.com/polars-unique/
#NAME PG009
#DESC unique：重複削除
#START
pl.Config.set_tbl_rows(5)
 
# データ読み込み
df = pl.read_csv("./csv/sns_diamonds.csv")
ans1 = df

# cut列の重複削除
ans2 = df.unique(subset="cut")
ans3 = df.unique(subset=["cut", "color"])

#END

https://datasciencemore.com/polars-melt-pivot/
#NAME PG010
#DESC melt, pivot：縦横変換
#START

# melt
df_wide = pl.DataFrame(
  {
    "store":["A", "B", "C"],
    "orange":[100, 70, 120],
    "apple":[150, 90, 80]
  }
)

# wide型をlong型に変換
df_long = df_wide.melt(
    id_vars="store",
    value_vars=["orange", "apple"],

    variable_name="fruit",
    value_name="price"
)
 
# データフレーム確認
ans1 = "melt", df_long

# pivot

# long型をwide型に変換
df_long.pivot(
    index="store",
    columns="fruit",
    values="price"
)

ans2 = "pivot", df_long

#END


https://datasciencemore.com/polars-str-slice/
#NAME PG011
#DESC str
#START
# シリーズ
series = pl.Series(["qwertyuiop@"])

# 抽出 前１文字目から4個
ans1 = series.str.slice(1, 4)

# 抽出 後ろ１０文字目から4個
ans2 = series.str.slice(-10, 4)

# シリーズ
series = pl.Series(["a", "the", "apple"])

# 長さ取得
# ans3 = series.str.n_chars()

series = pl.Series(["nogi", "sakura", "hinata"])

ans4 = series.str.concat()
ans5 = series.str.concat("_")

# マッチの真偽 aが入っているか
ans6 = series.str.contains("a")

series = pl.Series(["asuka", "mizuki", "minami"])

ans7 = series.str.replace("a", "A")

ans8 = series.str.replace_all("a", "A")

ans9 = series.str.replace_all("a", "A").str.replace_all("m", "M")

ans10 = series.str.split("u")

# マッチの分割 uにマッチした部分で分割（inclusive=True）
ans11 = series.str.split("u", inclusive=True)


#END

https://datasciencemore.com/polars-apply-series/
#NAME PG012
#DESC apply：シリーズの行処理
#START
df = pl.read_csv("./csv/sns_diamonds.csv")
series = df.get_column("color")

def func(x):
  if x == "E":
    return("E")
  elif x == "I":
    return("I")
  else:
    return("not_E_I")
 
# apply適用
#series.apply(func)
#series.map_elements(func)

#END


https://datasciencemore.com/polars-apply-dataframe/
#NAME PG013
#DESC apply：データフレームの行処理
#START
dft = pl.read_csv("./csv/sns_diamonds.csv")
df = dft.select("depth", "color")

def func(x):
    if x[1] == "E":
        return x[0]
    elif x[1] == "I":
        return 0
    else:
        return 1

ans1 = df.apply_row(func).to_series()

#END


#NAME PG014
#DESC
#START
pass
#END


#NAME PG015
#DESC
#START
pass
#END


#NAME PG016
#DESC
#START
pass
#END


#NAME PG017
#DESC
#START
pass
#END


#NAME PG018
#DESC
#START
pass
#END


#NAME PG019
#DESC
#START
pass
#END


#NAME PG020
#DESC
#START
pass
#END


#NAME PG021
#DESC
#START
pass
#END


#NAME PG022
#DESC
#START
pass
#END


#NAME PG023
#DESC
#START
pass
#END


#NAME PG024
#DESC
#START
pass
#END


#NAME PG025
#DESC
#START
pass
#END


#NAME PG026
#DESC
#START
pass
#END


#NAME PG027
#DESC
#START
pass
#END


#NAME PG028
#DESC
#START
pass
#END


#NAME PG029
#DESC
#START
pass
#END


#NAME PG030
#DESC
#START
pass
#END



<!--

#TITLE

#GLOBAL_NAME
#GLOBAL_START
#GLOBAL_END

#NAME PG000
#DESC 
#START
pass
#END

config.set_short_ans(True)

-EXIT

-->

