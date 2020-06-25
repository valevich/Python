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

line1 = ""

for filename in os.listdir("/Users/henryvalevich/Downloads/Temp/"):
    
    if filename.endswith(".m3u"):
        
        tempfile = open("output.txt","w")
        renam = "no"
        with open(filename, 'r') as searchfile:
            print ("----------- FILE PROCESSING ------- " + filename)
            i = 0
            n = 0
            x = 0
            for line in searchfile:
        
                if i == 0:
                    tempfile.writelines(line)
                
                if '#EXTINF:' in line:
                    line1 = line
                                
                if 'http://' in line:
                    i += 1
                    if '.mkv' in line: 
                        x += 1
                    elif '.mp4' in line: 
                        x += 1
                    elif '.avi' in line: 
                        x += 1
                    else:
                        tempfile.writelines(line1)
                        tempfile.writelines(line)
                        n += 1

#                    oldname = line.replace("http://","")
#                    oldname = oldname.replace(":","-")
#                    str_idx = int(oldname.find("/"))
#                    newname = (oldname[:str_idx] + "_" + str(i) + "_" + date_time + ".m3u")
#                    renam = "yes"

#            if renam == "yes":
#                print ("filename: " + filename)
#                print ("newname: " + newname)
#                os.rename(filename, newname)

            searchfile.close

            os.rename("output.txt", ("-" + filename))
            tempfile.close()
            print ("Input Channels: " + str(i))
            print ("Output Channels: " + str(n))
            print ("Bypassed Channels: " + str(x))
                    