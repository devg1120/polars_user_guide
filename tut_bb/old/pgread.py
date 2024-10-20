import re


def main():

    file = "pg.py"
    (l,d) = pg_read(file)
    print(l)
    print(d)


def pg_read(file):
    #file = "pg.py"
    
    prg_list = []
    prg_dict = {}
    
    #with open(file,encoding='utf-8') as f:
    try:
        f = open(file,encoding='utf-8') 
        lines = f.readlines()
        pgline = False
        comment = False
        pgsource = ""
        name = ""
        for line in lines:
            if re.match("<!--",line):
                comment = True 
            elif re.match("-->",line):
                comment = False
            if comment:
                continue
            #print(line.rstrip())
            if re.match("#NAME",line):
                #print("             match #NAME")
                r = re.match(r"^\#NAME\s+(\S+)",line)
                name = r.group(1)
                #print(name)
            elif re.match("#START",line):
                #print("             match #START")
                pgline = True
                pgsource = ""
            elif re.match("#END",line):
                #print("             match #END")
                pgline = False
                print("name", name)
                print("pgsource",pgsource)
                prg_list.append(name)
                prg_dict[name] = pgsource
            else:
                if pgline:
                    pgsource += line
    except Exception as e:
        print(e)

    return (prg_list, prg_dict)



if __name__ == "__main__":
    main()
