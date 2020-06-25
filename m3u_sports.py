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
line2 = ""

allowed = ['NBCSN','NBC Sports','NBC GOLD','ESPN','Fox Soccer','Fox Sports', \
            'Gol TV','MSG','NHL','Tennis','TUDN','Zona Futbol', \
            'Setanta Sports','AD SPORT','DIRECTV SPORTS','Rai Sport', \
            'Eurosport','ELEVEN SPORTS','Sky Sport','Sky Bundesliga', \
            'RMC SPORT1','BEIN','LFC TV','MUTV','BT SPORTS','BT SPORT', \
            'Ziggo Sport','EPL','RUSH SPORTS']
    

for filename in os.listdir("/Users/henryvalevich/Downloads/Temp/"):
    
    if filename.endswith(".m3u") or filename.endswith(".m3u8"):
        
        tempfile = open("output.txt","w")
        renam = "no"
        
        with open(filename, 'r') as searchfile:
        
            print ("----------- FILE PROCESSING " + filename + "------- ")
            i = 0
            n = 0
            xLinks1 = 0
            xLinks2 = 0
            
            for line in searchfile:
        
                if i == 0:
                    i += 1
                    tempfile.writelines(line)
                
                if '#EXTINF:'.casefold() in line.casefold():
                    for item in allowed:    
                        if item.casefold() in line.casefold():
                            line1 = line
                            n += 1

                if '#EXTGRP:'.casefold() in line.casefold():
                    if n > 0:
                        line2 = line
                        n += 1
                                
                if 'http://'.casefold() in line.casefold():
                    if n == 1:
                        tempfile.writelines(line1)
                        tempfile.writelines(line)
                        xLinks2 += 1
                    elif n > 1:
                        tempfile.writelines(line1)
                        tempfile.writelines(line2)
                        tempfile.writelines(line)
                        xLinks2 += 1
                        
                    n = 0
                    xLinks1 += 1
                        	

            searchfile.close
            os.rename("output.txt", ("-" + filename))
            tempfile.close()
            print ("Input Channels: " + str(xLinks1) + " ---> Sport Channels: " + str(xLinks2))
                    