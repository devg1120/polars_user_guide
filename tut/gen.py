
N = 30


print("#TITLE  DEMO")
print("")

for i in range(N):
    pgn = "PG" + str(i + 1).zfill(3)
    print("#NAME " + pgn)
    print("#DESC")
    print("#START")
    print("pass")
    print("#END")
    print("")
    print("")
    

ref = """
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
"""
print(ref)

