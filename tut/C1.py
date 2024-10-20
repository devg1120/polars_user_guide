
https://cloraordinary.com/python-polars-tips#google_vignette

https://datasciencemore.com/polars-join/

#TITLE  DEMO

#NAME PG001
#DESC dataframeの作成
#START
data = {"cols1": ["a", "b"], "cols2": [1, 2]}
df = pl.DataFrame(data)
ans1 = df

# 型指定
data = {"col1": [1, 2], "col2": [3, 4]}
df = pl.DataFrame(data, schema={"col1": pl.Float32, "col2": pl.Int64})
ans2 = df
#END


#NAME PG002
#DESC filter
#START
data = {"foo": [1,2,3,4,5,6,7,8,9], 
        "ham": ["a","b","c","a","b","c","a","b","c"],
        }
df = pl.DataFrame(data)
ans1 = df
ans2 = df.filter(pl.col("foo") > 6)

# 複数条件 
ans3 = df.filter((pl.col("foo") < 3) & (pl.col("ham") == "a"))
#END


#NAME PG003
#DESC 新規カラムの作成
#START
data = {"a": [1, 2], "b": [3, 4]}
df = pl.DataFrame(data)
ans1 = df
ans2 = df.with_columns((pl.col("a") ** 2).alias("c"))

list = [100,200]
ans3 = df.with_columns(pl.Series(name='new_col', values=list))

#END


#NAME PG004
#DESC 型変換(cast)
#START
data = {"a": [1, 2], "b": [3, 4]}
df = pl.DataFrame(data)
ans1 = df
ans2 = df.with_columns([pl.col("a").cast(pl.Float32)])
#END


#NAME PG005
#DESC データフレームの結合(join)
#START

data1 = {"a": [1, 2], "b": [3, 4]}
df1 = pl.DataFrame(data1)
data2 = {"a": [1, 2], "c": [5, 6], "d": [7, 8]}
df2 = pl.DataFrame(data2)

ans1  = df1
ans2  = df2
ans3 = "left" , df1.join(df2, how='left' , on=['a'])
ans4 = "right", df1.join(df2, how='right', on=['a'])
ans5 = "inner", df1.join(df2, how='inner', on=['a'])
ans6 = "outer", df1.join(df2, how='outer', on=['a'])


#END


#NAME PG006
#DESC データフレームの結合(join)
#START

data1 = {"a": [1, 2], "b": [3, 4]}
df1 = pl.DataFrame(data1)
data2 = {"a": [1, 2, 3], "c": [5, 6, 100], "d": [7, 8, 101]}
df2 = pl.DataFrame(data2)

ans1  = df1
ans2  = df2
ans3 = "left" , df1.join(df2, how='left' , on=['a'])
ans4 = "right", df1.join(df2, how='right', on=['a'])
ans5 = "inner", df1.join(df2, how='inner', on=['a'])
ans6 = "outer", df1.join(df2, how='outer', on=['a'])

#END


#NAME PG007
#DESC 結合(concat)
#START
data1 = {"a": [1, 2], "b": [3, 4]}
df1 = pl.DataFrame(data1)
data2 = {"a": [5, 6, 7], "b": [8, 9, 10]}
df2 = pl.DataFrame(data2)
data3 = {"c": [1, 2], "d": [3, 4]}
df3 = pl.DataFrame(data3)

ans1 = pl.concat([df1,df2])
ans2 = pl.concat([df1, df3], how="horizontal")

#END


#NAME PG008
#DESC カラム名のリネーム(rename)
#START
data = {"a": [1, 2], "b": [3, 4]}
df = pl.DataFrame(data)

ans1 = df

ans2 = df.rename({'a': 'a_x', 'b': 'b_x'})

#END


#NAME PG009
#DESC ソート(sort)
#START
data = {"a": [1, 5, 2, 9], "b": [30, 40, 10, 70]}
df = pl.DataFrame(data)

ans1 = df
ans2 = df.sort("a")
ans3 = df.sort("b")
ans4 = df.sort("a", descending=True)
ans5 = df.sort("b", descending=True)
ans6 = df.sort([pl.col("a"), pl.col("b")],descending=[False, True]) 
ans7 = df.sort([pl.col("a"), pl.col("b")],descending=[True, False]) 

#END


#NAME PG010
#DESC groupby.agg
#START
data = {"group": ["a", "a", "a", "b", "b", "b"], "value": [1, 2, 3, 4, 5, 6]}
df = pl.DataFrame(data)
ans1 = df

ans2 = df.group_by("group", maintain_order=True).agg(
        [
            pl.sum("value").name.suffix("_sum"),   # groupごとにvalueを合算
            pl.mean("value").name.suffix("_mean"), # groupごとのvalueの平均
            pl.count("value").alias("count"), # groupごとのvalueの数
            pl.n_unique("value").alias("unique_count"), # groupごとのユニークなvalueの数
        ]
)
#END


#NAME PG011
#DESC sort groupby.agg
#START
data = {"group": ["a", "a", "a", "b", "b", "b"], 
        "id": [100, 101, 102, 103, 104, 105], 
        "value": [1, 2, 3, 4, 5, 6]}
df = pl.DataFrame(data)
ans1 = (df.sort("value", descending=True) # valueを降順で並び替える
        .group_by('group').agg([pl.col('id').head(2).alias('labels')]) # groupごとに上からidの値を抜き出し、labelsカラムに格納する
     )

pass
#END


#NAME PG012
#DESC 列の削除
#START
data = {"cols1": ["a", "b"], "cols2": [1, 2], "cols3": ["zzz","xxx"]}
df = pl.DataFrame(data)
ans1 = df
ans2 = df.drop('cols2')

#END


#NAME PG013
#DESC 欠損値の確認
#START
df = pl.read_csv("./pokemon.csv")
null_counts = df.select([
    pl.col(name).is_null().sum().alias(name + "_null_count") 
    for name in df.columns
])

result = ""
# 各カラムのnull数を改行して表示
for column in null_counts.columns:
    #print(f"{column}: {null_counts[column][0]}")
    result += f"{column}: {null_counts[column][0]}" + "\n"

ans1 = result

# 欠損値のカラム削除
df2 = df.drop_nulls()

null_counts = df2.select([
    pl.col(name).is_null().sum().alias(name + "_null_count") 
    for name in df2.columns
])

result = ""
# 各カラムのnull数を改行して表示
for column in null_counts.columns:
    #print(f"{column}: {null_counts[column][0]}")
    result += f"{column}: {null_counts[column][0]}" + "\n"

ans2 = result
#END


#NAME PG014
#DESC map_elements
#START
# 簡単なデータフレームの作成
df = pl.DataFrame({
    "text": ["apple", "banana", "cherry", "date"]
})

# 特定の値のセットを作成
fruit_set = {"apple", "cherry"}

# map_elementsを使って1と0を割り当てる
ans1 = df.with_columns(
    pl.col("text").map_elements(lambda x: 1 if x in fruit_set else 0, return_dtype=pl.Int8).alias("is_fruit")
)


#END


#NAME PG015
#DESC 展開(explode)
#START
data = {"group": ["a"], 
        "value": [[1, 2, 3]]}
df = pl.DataFrame(data)
ans1 = df
ans2 = df.explode("value")

#END


#NAME PG016
#DESC カラム同士を演算
#START
data = {"col1": [1, 2], "col2": [3, 4]}
df = pl.DataFrame(data)
ans1 = df
ans2 = df.with_columns((df.get_column("col1") + df.get_column("col2")).alias("col1+col2"))


#END


#NAME PG017
#DESC スペース区切りの文章をリスト化
#START
data = {"cols": ["a b c"]}
df = pl.DataFrame(data)
ans1 = df
#ans2 = df.with_columns(pl.col('cols').apply(lambda s: s.split()).alias("cols_new")) 
ans2 = df.with_columns(pl.col('cols').map_elements(lambda s: s.split()).alias("cols_new")) 

#END


#NAME PG018
#DESC 値をリストで取り出す
#START
data = {"col1": [1, 2,3,4,5], "col2": [10,20,30,40,50]}
df = pl.DataFrame(data)
col_list = df["col2"].to_list()

ans1 = df
ans2 = col_list



#END


#NAME PG019
#DESC グループごとに通し番号を振る
#START
data = {"group": ["a", "a", "a", "b", "b", "b"], 
        "value": [1, 2, 3, 4, 5, 6]}
df = pl.DataFrame(data)

ans1 = (df.with_columns([pl.lit(1).alias("n")]) # 後の、cum_sum関数のために、1で埋めたnカラムを作成
        .with_columns(pl.col("n").cum_sum().over("group").alias("serial")) # groupごとの通し番号をserialカラムとして追加
     )

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

