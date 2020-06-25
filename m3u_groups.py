import os
import sys
from datetime import datetime

print ("=====================  START  =====================")
now = datetime.now() # current date and time
date_time = now.strftime("%m%d%Y")

#path = "/users/henryvalevich/Downloads/Temp"
path = str(input("Enter Path: [default: 1-Temp Current, 2-Temp or Enter Path] \n")).lower().strip()
if len(path) == 0 :
    path = "/Users/henryvalevich/Downloads/Temp Current/"
elif path == "1":
    path = "/Users/henryvalevich/Downloads/Temp Current/"
elif path == "2":
    path = "/Users/henryvalevich/Downloads/Temp/"

if os.path.exists(path):
    print('Path: ' + path) 
else:
    print('Path Does Not Exist!')
    sys.exit()

retval = os.getcwd()
print ("Current working directory %s" % retval)
os.chdir( path )
retval = os.getcwd()
print ("Directory changed successfully %s" % retval)

xParam = input("Enter Group: [default:FOOTBALL] \n")
#if xParam == '':
#    print ("Parameter is missing!")
#    sys.exit() 

if len(xParam) == 0 :
    xParam = "FOOTBALL"
    
    
fno = 0
firstfile = "Y"

for filename in sorted(os.listdir(path)):

    if filename.endswith(".m3u") or filename.endswith(".m3u8"):
        
        tempfile = open("output.txt","w")
        fno += 1
        with open(filename, 'r') as searchfile:

            print ("----------- FILE PROCESSING: " + filename + "----------")
            line1 = ""
            line2 = ""
            line3 = ""
            tempfile.writelines("")
            
            for line in searchfile:                        

                if not line.strip():
                    continue
                    
                if '#EXTM3U' in line:
                    continue

                if '#EXTINF:'.casefold() in line.casefold():
                    line1 = line.rstrip()
                    continue

                if '#EXTGRP:'.casefold() in line.casefold():
                    line2 = line.rstrip()
                    continue

                if 'http://'.casefold() in line.casefold():
                    line3 = line.rstrip()
                    if not line2:
                        line2 = ("#EXTGRP:FOOTBALL")
                    tempfile.writelines(line1 + "\n")
                    tempfile.writelines(line2 + "\n")
                    tempfile.writelines(line3 + "\n")
                    line1 = ""
                    line2 = ""
                    line3 = ""
    
            tempfile.close
            searchfile.close
            tempfile.close()
            os.remove(filename)
            os.rename("output.txt", filename)


print ("---------------------------------------------------")
print ("Total Files: " + str(fno))
print ("---------------------------------------------------")
                    