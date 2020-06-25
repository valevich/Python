#!/usr/local/bin/python

import os
from datetime import datetime
print ("=====================  START  =====================")
now = datetime.now() # current date and time
date_time = now.strftime("%m%d%Y")

path = "/users/henryvalevich/Downloads/Temp"
retval = os.getcwd()
print ("Current working directory %s" % retval)

os.chdir( path )
retval = os.getcwd()
print ("Directory changed successfully %s" % retval)

xline = ""

toremove = ['https://flylinks.net,','https://flylinks.net, ','https://flylinks.net - ']
    

for filename in os.listdir("/Users/henryvalevich/Downloads/Temp/"):
    
    if filename.endswith(".m3u") or filename.endswith(".m3u8"):
        
        tempfile = open("output.txt","w")
        renam = "no"
        
        with open(filename, 'r',encoding="ISO-8859-1") as searchfile:
        
            print ("----------- FILE PROCESSING " + filename + "------- ")
            
            for line in searchfile:
        
                line = ''.join([s for s in line if ord(s) < 127])
                xline = line
                if '#extinf:'.casefold() in line.casefold():
                    for item in toremove:    
                        if item.casefold() in line.casefold():
                            xline = line.replace(item,"")
                            print ("line: " + line + " Replaced: " + xline)
                            
                tempfile.writelines(xline)                        

            searchfile.close
            os.remove(filename)
            os.rename("output.txt", (filename))
            tempfile.close()
                    