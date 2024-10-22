import sys
import re
import pf as PF
###############################################
def help():
   print("python exec_text.py -h")
   print("python exec_text.py <file>    //exec walk")
   print("python exec_text.py <file> 3  //exec one shot")
   print("python exec_text.py <file> -i //index dump")
   print("python exec_text.py <file> -t //exec through")
   print("python exec_text.py <file> -s //souce dump")
   sys.exit()

def main():
   args = sys.argv
   file = None
   gv = None
   gv_start_end = None
   silent = False
   through = False
   source = False
   if len(args) <2:
       sys.exit()

   if len(args) >= 2:
      arg1 = args[1]
      if arg1 == "-h":
          help()
      file = arg1

   #(title, pg_list, pg_dict, desc_dict) = PF.pg_read(file)
   """
   if len(args) == 3:
      arg2  = args[2]
      if arg2 == "-i":
          silent = True
      elif arg2 == "-t":
          through = True
      else:
         if not arg2.isdecimal():
             print(arg2, " not decimal")
             sys.exit()
         gv = "PG" + arg2.zfill(3)
   """

   if len(args) == 3:
      arg2  = args[2]
      if arg2 == "-i":
          silent = True
      elif arg2 == "-t":
          through = True
      elif arg2 == "-s":
          source = True
      else:
         if arg2.isdecimal():
             #gv = "PG" + arg2.zfill(3)
             gv = arg2
         else:
           m = re.match("([0-9]+)-([0-9]+)", arg2);
           if m != None:
               print("start:",m.group(1))
               print("end  :",m.group(2))
               start = m.group(1)
               end   = m.group(2)
               gv_start_end = (start, end)
           else:
               print(arg2, " not correct")
               sys.exit()

   (title, pg_list, pg_dict, desc_dict) = PF.pg_read(file)

   if gv != None:
     gvs = "PG" + gv.zfill(3)
     if gvs in pg_list:
          pg_list = [gvs]
     else:
          print(f"{gv}: testcase not exit")
          sys.exit()

   if gv_start_end != None:
        tmp_list = []
        start = int(gv_start_end[0])
        end   = int(gv_start_end[1])
        for pg in pg_list:
           m = re.match("^PG([0-9]+)", pg);
           if m != None:
               n = int(m.group(1))
               if start <= n and n <= end:
                   tmp_list.append(pg)
        print(tmp_list)
        pg_list = tmp_list

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
      if through :
         PF.epna_t(test_case,PG, DESC )
      else:
         PF.epna(test_case,PG, DESC, last, silent, source)
   

###############################################
###############################################

if __name__ == "__main__":
    main()
