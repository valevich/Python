import os
import vlc
import time
import urllib
import urllib.request
import validators
#import socket
#socket.setdefaulttimeout(5)

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

prevfile = ""
prevline = ""
fno = 0

for filename in os.listdir("/Users/henryvalevich/Downloads/Temp/"):
    
    if filename.endswith(".m3u") or filename.endswith(".m3u8"):
        
        line1 = ""
        line2 = ""
        line3 = ""
        fno += 1

        print ("---------------- START FILE PROCESSING ----------------")
        with open(filename, 'r',encoding="ISO-8859-1") as searchfile:

            xOK = 0
            xDead = 0
            
            tempfile1 = open("output1.txt","w")
            tempfile2 = open("output2.txt","w")

            for line in searchfile:                        

                xValid = ""
                try:
                
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
                        if 'http://blank' in line:
                            tempfile1.writelines(line1 + "\n")
                            if line2.strip():
                                tempfile1.writelines(line2 + "\n")
                            tempfile1.writelines(line3 + "\n")
                            continue

                        url = line
                        if not validators.url(url):
                            print ("not valid")
                            xValid = "N"
                        code = urllib.request.urlopen(url).getcode()

                        if str(code).startswith('2') or str(code).startswith('3'):
                            xValid = "Y"
                        else:
                            xValid = "N"
                
                except urllib.error.HTTPError as err:
                    xValid = "N"

                except urllib.error.URLError as e: 
                    xValid = "N"

                except ValueError: 
                    xValid = "N"
                    
                except OSError as err:
                    xValid = "N"

                
                if xValid == "Y":
                    print("ok : " + url.rstrip('\r\n'))
                    xOK += 1
                    tempfile1.writelines(line1 + "\n")
                    if line2.strip():
                        tempfile1.writelines(line2 + "\n")
                    tempfile1.writelines(line3 + "\n")
                elif xValid == "N":
                    xDead += 1
                    print("bad: " + url.rstrip('\r\n'))
                    tempfile2.writelines(line1 + "\n")
                    if line2.strip():
                        tempfile2.writelines(line2 + "\n")
                    tempfile2.writelines(line3 + "\n")
                    

            line1 = ""
            line2 = ""
            line3 = ""
                

                
            print ("---------------------------------------------------")
            print ("Total Valid Links: " + str(xOK))
            print ("Total Dead Links:  " + str(xDead))
                
            searchfile.close

#            tempfile1.close()
#            tempfile2.close()
            os.rename("output1.txt", ("ok-" + filename))
            os.rename("output2.txt", ("dead-" + filename))


print ("---------------------------------------------------")
print ("Total Files: " + str(fno))
print ("---------------------------------------------------")
                    