import os
import re
from datetime import datetime
os.system('clear')

path = "/Users/henryvalevich/Downloads/Temp Sports/"

print ("=====================  START  =====================")
now = datetime.now()
date_time = now.strftime("%m%d%Y")
retval = os.getcwd()
print ("Current working directory %s" % retval)
os.chdir( path )
retval = os.getcwd()
print ("Directory changed successfully %s" % retval)



#==========================================  MERGEFOLDERS FUNCTION  ==========================================
def mergeFolders_function():

    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~  BEGIN PROCESS: " + "(mergeFolders_function) ~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    path1 = "/Users/henryvalevich/Downloads/Temp/"
    path2 = "/Users/henryvalevich/Downloads/Temp Sports/"

    for filename in sorted(os.listdir(path1)):

        if filename.endswith(".m3u") or filename.endswith(".m3u8"):

            if (os.path.isfile(path2 + filename)):
                print("Error: %s file already exists" % filename)
                continue
                
            print ("Copying File: " + filename)
            os.replace(path1 + filename, path2 + filename)


    print ("")



#==========================================  DUPESREMOVE1 FUNCTION  ==========================================
def dupesremove1_function():

    fno = 0
    totalines = 0

    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~  BEGIN PROCESS: " + "(dupesremove1_function) ~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


    tempfile = open("tempsort.txt","w")

    for filename in sorted(os.listdir(path)):
    
        if filename.endswith(".m3u") or filename.endswith(".m3u8"):
        
            line1 = ""
            line2 = ""
            line3 = ""

            fno += 1
            with open(filename, 'r',encoding="ISO-8859-1") as searchfile:

                lno = 0
                for line in searchfile:                        

                    line = ''.join([s for s in line if ord(s) < 127])
                    
                    if '#EXTINF:'.casefold() in line.casefold():
                        res1 = line.rstrip()
                        res1 = res1.replace("|","")
                        res1 = res1.replace("-","")
                        res2 = res1.partition(",")[2]
                        line1 = "#EXTINF:0, " + res2.lstrip()
                        continue

                    if '#EXTGRP:'.casefold() in line.casefold():
                        line2 = line.rstrip()
                        continue


                    if 'http://'.casefold() in line.casefold():
                        if 'http://blank'.casefold() not in line.casefold():
                            if not line2:
                                line2 = "#EXTGRP:FOOTBALL"
                            line3 = line.rstrip()
                            tempfile.writelines(line1 + "|" + line2 + "|" + line3 + "\n")
                            lno += 1
                            totalines += 1
                            line1 = ""
                            line2 = ""
                            line3 = ""
        
                searchfile.close
                print ("file = " + filename + " - lines = " + str(lno))
             
                os.remove(filename)
                

    tempfile.close

    print ("---------------------------")
    print ("Total Files: " + str(fno))
    print ("Total Lines: " + str(totalines))
    print ("---------------------------")
    print ("")



#==========================================  SORT FUNCTION  ==========================================
def sort_function():

    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~  BEGIN PROCESS: " + "(sort_function) ~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    from operator import itemgetter
    totalines = 0
    prevcol3 = ""
    d=[]

    with open("tempsort.txt",'r',encoding="ISO-8859-1") as infile:
        for line in infile.readlines():
            totalines += 1
            data = line.strip().split('|')
            d.append(data)
    d.sort(key=itemgetter(2))

    with open('tempsort2.txt','w') as outfile:
        for line in d:
            xline = ('|'.join(line)+'\n')
            str_idx1 = int(xline.find("|"))
            str_idx2 = int(xline.find("http://"))
            col1 = (xline[:str_idx1])            
            col2 = (xline[str_idx1+1:str_idx2-1])
            col3 = (xline[str_idx2:])
            outfile.writelines(col1 + '|' + col2 + '|' + col3)


    print ("---------------------------")
    print ("Total Lines: " + str(totalines))
    print ("---------------------------")
    print ("")





#==========================================  DUPESREMOVE3 FUNCTION  ==========================================
def dupesremove2_function():
    
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~  BEGIN PROCESS: " + "(dupesremove2_function) ~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    fno = 0
    prevcol3 = ""
    prevline = ""


    with open('tempsort2.txt','r',encoding="ISO-8859-1") as infile:

        for line in infile.readlines():

            if line == prevline:
                continue
            else:
                prevline = line
            
            str_idx1 = int(line.find("|"))
            str_idx2 = int(line.find("http://"))
            col1 = (line[:str_idx1])
            col2 = (line[str_idx1+1:str_idx2-1])
            col3 = (line[str_idx2:])
    
            col3short = (col3.rsplit('/', 1)[0])
            oldname = col3short.replace("http://","")
            oldname = oldname.replace(":","-")
            str_idx = int(oldname.find("/"))
            newname = (oldname[:str_idx] + "_" + str(fno) + ".m3u")
        
            if prevcol3 == "":
                outfile = open("outfile.txt","w+")  
                outfile.writelines(""+'\n')
                outfile.writelines("#EXTINF:0,********(" + col3[7:13] + ")********"+'\n')
                outfile.writelines("#EXTGRP:FOOTBALL"+'\n')
                outfile.writelines("http://blank"+'\n')
                prevcol3 = oldname[:str_idx]
                    

            if prevcol3 != oldname[:str_idx]:
                fno += 1
                print ("Creating Extract File: " + prevcol3)
                outfile.close()
                os.rename("outfile.txt", prevcol3 + "_" + str(fno-1) + ".m3u")
                prevcol3 = oldname[:str_idx]

                outfile = open("outfile.txt","w+")  
                outfile.writelines(""+'\n')
                outfile.writelines("#EXTINF:0,********(" + col3[7:13] + ")********"+'\n')
                outfile.writelines("#EXTGRP:FOOTBALL"+'\n')
                outfile.writelines("http://blank"+'\n')


            outfile.writelines(col1+'\n')
            if not col2:
                outfile.writelines("#EXTGRP:FOOTBALL"+'\n')
            else:
                outfile.writelines(col2+'\n')
            outfile.writelines(col3)


    outfile.close()
    print ("Creating Extract File: " + prevcol3)
    os.rename("outfile.txt", prevcol3 + "_" + str(fno-1) + ".m3u")
    os.remove("tempsort.txt")
    os.remove("tempsort2.txt")

    print ("---------------------------")
    print ("Total Files: " + str(fno-1))
    print ("---------------------------")
    print ("")




if __name__ == "__main__":

    mergeFolders_function()
    
    dupesremove1_function()

    sort_function()

    dupesremove2_function()


                    