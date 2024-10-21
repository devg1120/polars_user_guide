
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
#ans5 = df1.with_columns(
#    new =
#    pl.when(pl.col("color") == "E")
#    .then("E")
#    .otherwise("not_E")
#)

#ans5 = df1.with_columns(
#    new =
#    pl.when(pl.col("color") == "E")
#    .then("E")
#    .when(pl.col("color") == "I")
#    .then("I")
#    .otherwise("not_E_I")
#)



#END


#NAME PG005
#DESC
#START
pass
#END


#NAME PG006
#DESC
#START
pass
#END


#NAME PG007
#DESC
#START
pass
#END


#NAME PG008
#DESC
#START
pass
#END


#NAME PG009
#DESC
#START
pass
#END


#NAME PG010
#DESC
#START
pass
#END


#NAME PG011
#DESC
#START
pass
#END


#NAME PG012
#DESC
#START
pass
#END


#NAME PG013
#DESC
#START
pass
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

