import os
from datetime import datetime

os.system('clear')
print ("=================================================================")
print ("======================   START M3U_RENAME  ======================")
print ("=================================================================")

now = datetime.now() # current date and time
date_time = now.strftime("%m%d%Y")

path = "/users/henryvalevich/Downloads/Temp"
retval = os.getcwd()
print ("Current working directory %s" % retval)

os.chdir( path )
retval = os.getcwd()
print ("Directory changed successfully %s" % retval)

fno = 0

for filename in os.listdir("/Users/henryvalevich/Downloads/Temp/"):
    
    if filename.endswith(".m3u") or filename.endswith(".m3u8"):
        
        fno += 1
        renam = "no"
        print ("------------------------------------------------")
        with open(filename, 'r') as searchfile:

            lineno = 0
            pre, ext = os.path.splitext(filename)
#            print ("Pre: " + pre)
#            print ("Ext: " + ext)
            
            for line in searchfile:
 
                line = ''.join([s for s in line if ord(s) < 127])
                
                if lineno == 3:
                    break
                                
                if 'http://' in line:
                    lineno += 1
                    oldname = line.replace("http://","")
                    oldname = oldname.replace(":","-")
                    str_idx = int(oldname.find("/"))
                    newname = (oldname[:str_idx] + "_" + str(fno) + "_" + date_time + ext)

            print ("Old Name: " + filename)
            print ("New Name: " + newname)
            os.rename(filename, newname)
            searchfile.close

print ("---------------------------------------------------")
print ("Total Files: " + str(fno))
print ("---------------------------------------------------")
                    