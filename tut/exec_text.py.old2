import sys
import re
import pf as PF
###############################################
def help():
   print("python exec_text.py -h")
   print("python exec_text.py 001.py")
   print("python exec_text.py 001.py 3")
   print("python exec_text.py 001.py -s")
   sys.exit()

def main():
   args = sys.argv
   file = None
   gv = None
   silent = False

   if len(args) <2:
       sys.exit()

   if len(args) >= 2:
      arg1 = args[1]
      if arg1 == "-h":
          help()
      file = arg1

   (title, pg_list, pg_dict, desc_dict) = PF.pg_read(file)
   #print(pg_list)
   #print(pg_dict)
   #print(desc_dict)

   if len(args) == 3:
      arg2  = args[2]
      if arg2 == "-s":
          silent = True
      else:
         gv = "PG" + arg2.zfill(3)
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


   #dataset = PF.pl.read_csv("../csv/pokemon.csv")
   #PF.gv["df"] = dataset

   if len(title) > 1 :
      print("")
      print("/********************************************/")
      print("/*** "+ title, end = "")
      print(" " * (37 - len(title)) + "***/")
      print("/********************************************/")

   for i,test_case in enumerate(pg_list):
      last = False
      if i == len(pg_list) -1:
          last = True
      PG =pg_dict[test_case]
      DESC =desc_dict[test_case]
      PF.epna(test_case,PG, DESC, last, silent)
   

###############################################
###############################################

if __name__ == "__main__":
    main()
