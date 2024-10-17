import sys
import re
import pf as PF
###############################################

def  main():
   args = sys.argv
   file = None
   gv = None

   if len(args) <2:
       sys.exit()

   if len(args) >= 2:
      file = args[1]

   (pg_list,pg_dict) = PF.pg_read(file)
   #print(pg_list)
   #print(pg_dict)

   if len(args) == 3:
      num  = args[2]
      gv = "PG" + num.zfill(3)
      #print(gv)
      if gv in pg_list:
          pg_list = [gv]
      else:
          print(f"{gv}: testcase not exit")
          sys.exit()


   pgv_list = []

   if len(args) < 2:
       for gv in globals():
           if re.match("PG[0-9]+",gv):
               pgv_list.append(gv)
           #else:
           #    print(gv)
   else:
       num = args[1]
       gv = "PG" + num.zfill(3)
       pgv_list.append(gv)


   dataset = PF.pl.read_csv("../csv/pokemon.csv")
   PF.gv["df"] = dataset

   for i,test_case in enumerate(pg_list):
      last = False
      if i == len(pg_list) -1:
          last = True
      PG =pg_dict[test_case]
      PF.epna(test_case,PG, last)
   

###############################################
###############################################

if __name__ == "__main__":
    main()
