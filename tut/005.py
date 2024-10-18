##  template
<!--
#NAME PG
#DESC 
#START
#END
#TITLE Basic operator

#GLOBAL_NAME df
#GLOBAL_START
#GLOBAL_END
--EXIT
-->

#TITLE String

#NAME  PG001
#DESC  
#START
df = pl.DataFrame({"animal": ["Crab", "cat and dog", "rab$bit", None]})

out = df.select(
    pl.col("animal").str.len_bytes().alias("byte_count"),
    pl.col("animal").str.len_chars().alias("letter_count"),
)
print(out)
#END



#NAME PG002
#DESC  
#START
out = df.select(
    pl.col("animal"),
    pl.col("animal").str.contains("cat|bit").alias("regex"),
    pl.col("animal").str.contains("rab$", literal=True).alias("literal"),
    pl.col("animal").str.starts_with("rab").alias("starts_with"),
    pl.col("animal").str.ends_with("dog").alias("ends_with"),
)
print(out)
#END


#NAME PG003
#DESC 
#START
df = pl.DataFrame(
    {
        "a": [
            "http://vote.com/ballon_dor?candidate=messi&ref=polars",
            "http://vote.com/ballon_dor?candidat=jorginho&ref=polars",
            "http://vote.com/ballon_dor?candidate=ronaldo&ref=polars",
        ]
    }
)
out = df.select(
    pl.col("a").str.extract(r"candidate=(\w+)", group_index=1),
)
print(out)
#END


#NAME PG004
#DESC 
#START
df = pl.DataFrame({"foo": ["123 bla 45 asd", "xyz 678 910t"]})
out = df.select(
            pl.col("foo").str.extract_all(r"(\d+)").alias("extracted_nrs"),
            )
print(out)
#END

#NAME PG005
#DESC 
#START
df = pl.DataFrame({"id": [1, 2], "text": ["123abc", "abc456"]})
out = df.with_columns(
            pl.col("text").str.replace(r"abc\b", "ABC"),
            pl.col("text").str.replace_all("a", "-", literal=True).alias("text_replace_all"),
            )
print(out)
#END


#NAME PG006
#DESC 
#START
#END

#NAME PG007
#DESC 
#START
#END

#NAME PG008
#DESC  datetime
#START
#END


#NAME PG009
#DESC 
#START
#END


<!--
#NAME PG005
#DESC 
#START
#END
-->
