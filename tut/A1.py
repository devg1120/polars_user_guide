<!--
https://blog.deepblue-ts.co.jp/data-processing/polars-tutorial-with-to-be-careful/
-->

#TITLE Expr

#GLOBAL_NAME df
#GLOBAL_START
pl.DataFrame(
    {
        "ID": ["01","01","03"],
        "Name": [
            "tanaka",
            "yamamoto",
            "ueda",
            ],
        "Age": [ 45,33,58]
    }
)

#GLOBAL_END


#NAME PG001
#DESC Expr
#START

# Expression

expr1 = pl.col("ID", "Name")
# または
expr2 = pl.col(["ID", "Name"])
# または
expr3 = [pl.col("ID"), pl.col("Name")]

ans1 = df.select(expr1)
ans2 = df.select(expr2)
ans3 = df.select(expr3)

#END

#NAME PG002
#DESC  polarsのメソッド
#START

# メソッドの種類の注意点
# Polarsで用いるメソッド(処理)の書き方は以下の4種類があります。
# 以下の例のように、"mean"は4種全てがありますが、他のメソッドはそうでないものがほとんどですので、これらを混同しないように心がけましょう。
# また、返り値の違いも意識しましょう。

# polarsのメソッド。
# polars.Expressionのメソッド。
# polars.DataFrameのメソッド。
# polars.Seriesのメソッド。

# その1 polarsのメソッド。例：
mean_expr = pl.mean("Age") # -> Expr
ans1 = df.select(mean_expr)

# その2 polars.Expressionのメソッド。例：
self_mean_expr = pl.col("Age").mean() # -> self (Expr)
ans2 = df.select(self_mean_expr)

# その3 polars.DataFrameのメソッド。例：
ans3 = df.mean() # -> DataFrame

# その4 polars.Seriesのメソッド。例：
sr = pl.Series("a",[1,2,3])
ans4 = sr
#END

#NAME PG003
#DESC DataFrameの生成
#START

# 読み込み
# CSVファイル、JSONファイル、Excelファイルなどを読み込んで生成することができます。

input_csv = "input.csv"
df_csv = pl.read_csv(input_csv)
ans1 = df_csv
input_json = "input.json"
df_json = pl.read_json(input_json)
ans2 = df_json

#input_excel = "input.xlsx"
#df_excel = pl.read_excel(input_excel)
#ans3 = df_excel

#END


#GLOBAL_NAME data
#GLOBAL_START
{
    "店舗名": ["東京タワー店", "浅草寺店", "秋葉原店", "東京タワー店", "浅草寺店"],
    "曜日": ["土曜日", "土曜日", "日曜日", "日曜日", "土曜日"],
    "売上額": [500000, 300000, 450000, 600000, 350000],
    "客数": [200, 150, 180, 250, 160]
}
#GLOBAL_END


#NAME PG004
#DESC 
#START

# 変換
# 辞書型変数、Pandas.DataFrame、Numpy.ndarrayなどから変換して生成することができます。ただし、以下の例のように、それぞれの挙動が微妙に異なる点に注意しましょう。

df_dict1 = pl.DataFrame(data)

# または

df_dict2 = pl.from_dict(data)

ans1 = df_dict1
ans2 = df_dict2
#END

#NAME PG005
#DESC  DataFrameの出力
#START

# DataFrameの出力
# DataFrameはCSV, JSON, Excelなどに出力できます。

df = pl.DataFrame(data)

output_csv = "output.csv"
df.write_csv(output_csv)

output_json = "output.json"
df.write_json(output_json)

#END

#NAME PG006
#DESC DataFrameの基本情報
#START

# DataFrameの基本情報
# 行数と列数
# shapeというDataFrameのメソッドで行数と列数をタプルで取得できます。
# 行数と列数をバラでほしい場合は、heightやwidthというメソッドを使用できます。
#i lenでは行数を取得できます。

df = pl.DataFrame(data)   

ans1 = str(df.shape)
ans2 = str(len(df))
ans3 = str(df.height)
ans4 = str(df.width)
#END

#NAME PG007
#DESC DataFrameの基本情報
#START

# DataFrameの基本情報
# 列名とデータ型
# schemaというDataFrameのメソッドで列名とデータ型を辞書型で取得できます。
# 列名とデータ型をバラでほしい場合は、columnsとdtypesというメソッドを使用できます。

df = pl.DataFrame(data)   

ans1 = str(df.schema)
ans2 = str(df.columns)
ans3 = str(df.dtypes)
#END

#NAME PG008
#DESC 
#START

# 列の抽出
# DataFrameとして抽出
# selectメソッド
# 列を指定して抽出し、列数を減らします。selectというメソッドを用いますが、感覚的には「選択」というよりも「DataFrameを新たに生成」と考えるほうがしっくりきます。

df = pl.DataFrame(data)   
select_columns = ["店舗名", "曜日", "客数"]

ans1 = df.select(
    select_columns, 
)

column_1 = ["店舗名"]
column_2 = "曜日"
column_3 = pl.col("客数")

ans2 = df.select(
    column_1, column_2, column_3
)


select_columns_order = ["曜日", "店舗名", "客数", "売上額"]

ans3 = df.select(
    select_columns_order, 
)


exclude_columns = ["客数"]

qns4 = df.select(
    pl.exclude(exclude_columns)
)


select_elements = [
    "店舗名", 
    "曜日", 
    pl.col("売上額").alias("Sales")
]

ans5 = df.select(select_elements)

ans6 = df.select(
    pl.all()
)

#END

#NAME PG009
#DESC 
#START

# Seriesとして抽出
# get_columnというDataFrameのメソッドでは、指定した1列をSeriesとして作成します。
# 
# ただし、get_columnの引数は必ず列名(文字列型)でなければならず、pl.colなどのExpressionは使用できない点に注意しましょう。
# 
# また、複数列のSeriesを一つのget_columnで作成することはできません。
# 
# 似たような名前のメソッドとしてget_columnsがありますが、これはDataFrameの全部の列をSeriesのリストに変換するものなので、混同しないように注意しましょう。



df_example  = pl.DataFrame(data)   

ans1 = df_example.get_column("売上額")

culc_columns = [
    (
        pl.col("売上額") / pl.col("客数")
    ).alias("一人当たり売上"),
    (
        pl.col("売上額") % pl.col("客数")
    ).alias("売上の剰余")
]

ans2 = df_example.select(
    culc_columns
)

ans3 = df_example.select(
    pl.sum("売上額", "客数")
)


ans4 = df_example.select(
    pl.col("売上額", "客数").sum()
)


ans5 = df_example.select(
    pl.col("売上額", "客数")
).sum()


ans6 = df_example.get_column(
    "売上額"
).sum()


ans7 = df_example.describe()

ans8 = df_example.with_columns(
    pl.lit("東京").alias("都道府県")
)



ans9 = df_example.with_columns(
    pl.when(
        pl.col("売上額") == pl.max("売上額")
    ).then(
        pl.lit("売上が最高")
    ).when(
        pl.col("客数") == pl.max("客数")
    ).then(
        pl.lit("客数が最高")   # 実際には"売上が最高"が優先される
    ).when(
        pl.col("売上額") / pl.col("客数") == (pl.col("売上額") / pl.col("客数")).max()
    ).then(
        pl.lit("一人当たり売上が最高")
    ).otherwise(
        pl.col("店舗名") + pl.col("曜日")
    ).alias("備考欄")
)

#END


#NAME PG010
#DESC 
#START

df_example  = pl.DataFrame(data)   

#列の上書き
#aliasによる既存の列名の指定
#with_columnsで既存の列名を指定した場合、その列を上書きできます。
#更新前の列データは消えてしまう点に注意しましょう。

ans1 = df_example.with_columns(
    pl.lit(1000).alias("客数")
)

#END

#NAME PG011
#DESC 
#START

df_example  = pl.DataFrame(data)   

#aliasを使用しない場合
#Expressionの計算に対してaliasをしない場合、デフォルトの列名は「最初に登場したExpression」に基づきます。

#以下の例では、pl.col("売上額")が最初に登場するので、デフォルトの列名も"売上額"になります。
#すなわち、既存の"売上額"列のデータが上書きされます。


ans1 = df_example.with_columns(
    (
        pl.col("売上額") / pl.col("客数")
    )
)

#END

#NAME PG012
#DESC 
#START

df_example  = pl.DataFrame(data)   

# with_columnsの注意点
# with_columnsにはExpressionを複数渡すことができますが、その場合は各々が並列で処理されるため、互いを参照できないという点に注意しましょう。


ans1 = df_example.with_columns(
    pl.lit(1000).alias("客数"),
    (pl.col("売上額") / pl.col("客数")).alias("一人当たり売上")
)

#END

#NAME PG013
#DESC 
#START
df_example  = pl.DataFrame(data)   

# 行の選択
# sliceによる選択
# 行の選択にはsliceというDataFrameのメソッドを使います。
# 引数には開始行番号と行数の二つを渡します。

# 通常のlistをsliceする場合とは引数が異なるため注意しましょう。

ans1 = df_example.slice(1, 3)

#END

#NAME PG014
#DESC 
#START
df_example  = pl.DataFrame(data)   

# 最初や最後の行を選択
# head, tailというメソッドで、DataFrameの先頭または末尾の数行を選択します。
# 引数に行数を指定でき、デフォルトでは5行です。


ans1 = df_example.head(1)
ans2 = df_example.tail(1)

#END

#NAME PG015
#DESC 
#START
df_example  = pl.DataFrame(data)   

# sampleによるランダムな選択
# sampleというメソッドで、ランダムな数行を選択します。
# 最初の引数は行数で、それ以外の引数については割愛します。
# デフォルトでは1行です。

ans1 = df_example.sample()
#END

#NAME PG016
#DESC 
#START
df_example  = pl.DataFrame(data)   
# 行のフィルタリング
# filterによる条件付け
# filterというDataFrameのメソッドを用いて、条件に従って行を絞り込みます。
# 条件として文字列やExpressionとPythonの条件演算子(==, !=, >=, >, <=, <)などを用いることができます。
# filterにおける文字列はpl.lit(リテラル)として解釈されるようです。


ans1 = df_example.filter(
    pl.col("店舗名") != "東京タワー店"
)
#END

#NAME PG017
#DESC
#START
df_example  = pl.DataFrame(data)   

#条件式の組み合わせ
#&や|を使用して条件のExpressionを組み合わせることができます。ただし、NOTを表す演算子は!ではなく~です。

#また、これらを使用する際には、一つ一つの条件を()で囲まないとエラーになるので注意しましょう。


ans1 = df_example.filter(
    ~(pl.col("店舗名") == "東京タワー店") &
    (pl.col("売上額") >= pl.mean("売上額"))
)
#END

#NAME PG018
#DESC
#START
df_example  = pl.DataFrame(data)   

# uniqueによる要素の抽出
# uniqueというDataFrameのメソッドで、指定した列のデータが重複した行は一つを残して削除します。
# 引数に列名を渡すと、その列の重複のみを考慮します。
# 複数の列名を渡す場合はリストで渡します。
# 引数がない場合は全ての列が重複する場合のみ削除されます。


unique_columns = ["店舗名", "曜日"]
ans1 = df_example.unique(unique_columns)

#END

#NAME PG019
#DESC 
#START
df_example  = pl.DataFrame(data)   

# sortによる基本的な並べ替え
# sortまたはsort_byを使用して行を並べ替えます。
# 
# sortはDataFrameのメソッドとExpressionのメソッド(Expressionを返す)とがありますが、"pl."で始まる書き方は出来ないので注意しましょう。
# 
# その一方でsort_byはExpressionのメソッドです。
# 
# DataFrameのメソッドのsortは、引数に指定された列を基準にDataFrameの全ての列を並び替えます。
# これにはselect(pl.all().sort_by("列名"))が対応しています。
# なぜなら、sort_byは引数に指定された列を基準に複数の列を並び替えるExpressionだからです。
# 
# なお、これらのメソッドの引数に渡せる列名は文字列かExpressionかそれらのリストで、それ以外の引数として降順(decending)やnull(欠損値)を末尾に表示するかどうか(nulls_last)があります。
# 
# さらに、引数には複数の列を指定できます。
# 複数列が指定された場合は、左の引数(列名)から優先的に並べ替えられます。
# この際、decendingには基準にする列数と同じ長さのTrue/Falseのリストを渡すことによって、各列の降順/昇順を制御できます。

ans1 = df_example.sort("店舗名", "曜日")

# または

ans2 = df_example.select(pl.all().sort_by("店舗名", "曜日"))

#END

#NAME PG020
#DESC 
#START
df_example  = pl.DataFrame(data)   

#もう一つのsort
#ではExpressionのメソッドであるsortは何をするかというと、直前のExpressionで選択された全ての列をバラバラに並べ替えます。
#
#すなわち、行データを維持しないという点に注意しましょう。
#
#sort_byやDataFrameのメソッドのsortとは対応していないので、混同しないように注意しましょう。

ans1 = df_example.select(pl.all().sort())

#END


#NAME PG021
#DESC 
#START
df_example  = pl.DataFrame(data)   
# グループ化
# group_byというDataFrameのメソッドで、指定した列のデータに従って各行をグループ分けします。
# なお、group_byには複数の列を指定できます。
# 
# その直後にaggというメソッドを付けることで、各グループごとに総和、平均、最大値などを取得できます。
# 
# なお、グループの順番は毎回ランダムなのですが、group_byの後は指定した列を基準にsortすることで一定の結果を見られます。

ans1 = df_example.group_by("曜日").agg(
    pl.max("客数").alias("最大客数"),
    pl.mean("客数").alias("平均客数"),
    pl.sum("客数").alias("合計客数"),
).sort("曜日")
#END

#NAME PG022
#DESC 
#START
df_example  = pl.DataFrame(data)   
# ピボットテーブルの作成
# pivotによる列の指定
# pivotというDataFrameのメソッドで、ピボットテーブルを作成できます。
# 
# 引数として、indexは表側(行名)とする列名、columnsは表頭(列名)とする列名、valuesは値を参照する列名があります。
# 
# なお、複数の列を表側や表頭とする場合は、列名のリストを渡す必要があります。
# 
# さらに、オプション引数として、aggregate_functionはvaluesに対する総和、平均、最大値などの計算を指定できます。


df_pivot = df_example.pivot(
    values="売上額", index="店舗名", columns="曜日", aggregate_function="mean"
)

ans1 = df_pivot

# meltによるピボットテーブルの解除
# pivotの逆のことをするメソッドとしてmeltがあります。
# 
# meltの引数のid_varsはキーとする列、value_varsはデータとする列(指定しない場合はid_vars以外の全ての列)で、さらにvariable_nameやvalue_nameという引数で、下の例で"variable", "value"になっている列名を命名できます。


ans2 = df_pivot.melt(id_vars="店舗名")

#END


<!--
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
