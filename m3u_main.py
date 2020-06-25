import os
import re
from datetime import datetime
from shutil import copyfile
#from gdrive_updatefile import *

print ("=====================  START  =====================")
now = datetime.now() # current date and time
date_time = now.strftime("%m%d%Y")

path = "/users/henryvalevich/Downloads/Temp"
retval = os.getcwd()
print ("Current working directory %s" % retval)
os.chdir( path )
retval = os.getcwd()
print ("Directory changed successfully %s" % retval)


#==========================================  RENAME FUNCTION  ==========================================
def rename_function():

    fno = 0
    i = 0
    max = 21

    tempfile = open("output.txt","w")

    print ("")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~  BEGIN PROCESS: " + "(rename_function) ~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for filename in os.listdir(path):
    
        if filename.endswith(".m3u") or filename.endswith(".m3u8"):
        
            fno += 1
            renam = "no"

            with open(filename, 'r',encoding="ISO-8859-1") as searchfile:

                for line in searchfile:
        
                    if i < max:
                        i += 1
                        tempfile.writelines(line)
                    else:
                        i = 0
                        break
                                
                    if 'http://' in line:
                        oldname = line.replace("http://","")
                        oldname = oldname.replace(":","-")
                        str_idx = int(oldname.find("/"))
                        newname = (oldname[:str_idx] + "_" + str(fno) + "_" + date_time + ".m3u")
                        renam = "yes"

                if renam == "yes":
                    tempfile.writelines("#EXTINF:0,-------------- " + newname + " --------------\r\n")
                    tempfile.writelines("http://-----------------------------\r\n")
                    print ("filename: " + filename + " ---> newname: " + newname)
                    os.rename(filename, newname)

                searchfile.close

    os.remove("output.txt")
    tempfile.close()
    print ("---------------------------")
    print ("Total Files Renamed: " + str(fno))
    print ("---------------------------")
    print ("")


#==========================================  SPORTS FUNCTION  ==========================================
def sports_function():

    line1 = ""
    line2 = ""
    fno = 0

    allowed = ['NBCSN','NBC Sports','NBC GOLD','ESPN','Fox Soccer','Fox Sports', \
                'Gol TV','MSG','NHL','Tennis','TUDN','Zona Futbol', \
                'Setanta Sports','AD SPORT','DIRECTV SPORTS','Rai Sport', \
                'Eurosport','ELEVEN SPORTS','Sky Sport','Sky Bundesliga', \
                'RMC SPORT1','BEIN','LFC TV','MUTV','BT SPORTS','BT SPORT', \
                'Ziggo Sport','EPL','RUSH SPORTS']
    

    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~  BEGIN PROCESS: " + "(sports_function) ~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for filename in sorted(os.listdir(path)):
    
        if filename.endswith(".m3u") or filename.endswith(".m3u8"):
        
            fno += 1
            tempfile = open("output.txt","w")
            renam = "no"
        
            with open(filename, 'r',encoding="ISO-8859-1") as searchfile:
        
                i = 0
                n = 0
                xLinks1 = 0
                xLinks2 = 0
            
                for line in searchfile:
                    
                    line = ''.join([s for s in line if ord(s) < 127])
        
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
                            tempfile.writelines("#EXTGRP:FOOTBALL\n")
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
                print ("file: " + filename + " -> Total Links: " + str(xLinks1) + " - Sports Links: " + str(xLinks2))

                os.remove(filename)

    print ("---------------------------")
    print ("Total Files: " + str(fno))
    print ("---------------------------")
    print ("")
                    


#==========================================  DUPESMERGE FUNCTION  ==========================================
def dupesmerge_function():

    fno = 0
    firstfile = "Y"
    tempfile = open("output.txt","w")
    newline = ""
    prevfile = ""
    prevno = 0

    m3ufiles = [f for f in os.listdir(path) if re.search(r'.*\.(m3u|m3u8)$', f)]
#    print(len(m3ufiles))

    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~  BEGIN PROCESS: " + "(dupesmerge_function) ~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for filename in sorted(os.listdir(path)):
    
        if filename.endswith(".m3u") or filename.endswith(".m3u8"):
        
            fno += 1
            with open(filename, 'r',encoding="ISO-8859-1") as searchfile:

                str_idx = int(filename.find("_"))
                newname = (filename[:str_idx] + ".m3u")

                if newname != prevfile:
                    if firstfile != "Y":
                        if prevno > 1:
                            os.rename("output.txt", ("+" + prevfile))
                        else:    
                            os.rename("output.txt", ("-" + prevfile))
                        tempfile.close()
                        tempfile = open("output.txt","w")
                        prevno = 0

                prevfile = newname
                prevno += 1

                lineno = 0
                for line in searchfile:                        

                    lineno += 1
                    newline = line.replace("|","-")

                    if '#EXTM3U' in line:
                        if firstfile == "Y":
                            firstfile = "N"
                            print ("file = " + filename)
                        else:
                            print ("file = " + filename)
                    else:         
                        tempfile.writelines(newline)


                searchfile.close

                os.remove(filename)


    if prevno > 1:
        os.rename("output.txt", ("+" + prevfile))
    else:    
        os.rename("output.txt", ("-" + prevfile))

    tempfile.close()
    print ("---------------------------")
    print ("Total Files: " + str(fno))
    print ("---------------------------")
    print ("")



#==========================================  DUPESREMOVE1 FUNCTION  ==========================================
def dupesremove1_function():

    fno = 0

    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~  BEGIN PROCESS: " + "(dupesremove1_function) ~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for filename in sorted(os.listdir(path)):
    
        if filename.endswith(".m3u") or filename.endswith(".m3u8"):
        
            if filename.startswith("+"):
    
                line1 = ""
                line2 = ""
                line3 = ""

                fno += 1
                with open(filename, 'r',encoding="ISO-8859-1") as searchfile:


                    tempfile = open("tempsort.txt","w")
                    for line in searchfile:                        

                        if '#EXTINF:'.casefold() in line.casefold():
                            line1 = line.rstrip()
                            continue

                        if '#EXTGRP:'.casefold() in line.casefold():
                            line2 = line.rstrip()
                            continue

                        if 'http://'.casefold() in line.casefold():
                            line3 = line.rstrip()
                            tempfile.writelines(line1 + "|" + line2 + "|" + line3 + "\n")
                            line1 = ""
                            line2 = ""
                            line3 = ""
            
                    tempfile.close
                    searchfile.close
                    print ("file = " + filename)
                 

                pre, ext = os.path.splitext(filename)
                os.rename("tempsort.txt", pre + ".txt")


#            tempfile.close()

    print ("---------------------------")
    print ("Total Files: " + str(fno))
    print ("---------------------------")
    print ("")



#==========================================  DUPESREMOVE2 FUNCTION  ==========================================
def dupesremove2_function():
    
    from operator import itemgetter

    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~  BEGIN PROCESS: " + "(dupesremove2_function) ~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    fno = 0
    for filename in sorted(os.listdir(path)):

        if filename.endswith(".txt"):

            fno += 1
            prevcol3 = ""
            d=[]

            with open(filename,'r',encoding="ISO-8859-1") as infile:
                for line in infile.readlines():
                    data = line.strip().split('|')
                    d.append(data)
            d.sort(key=itemgetter(2))                 #sort the list `d` with the 2 item(3th column) of your sublist.

            with open('outfile.000','w') as outfile:
                for line in d:
                    xline = ('|'.join(line)+'\n')
                    str_idx1 = int(xline.find("|"))
                    str_idx2 = int(xline.find("http://"))
                    col1 = (xline[:str_idx1])
                    col2 = (xline[str_idx1+1:str_idx2-1])
                    col3 = (xline[str_idx2:])
                    if col3 != prevcol3:
                        outfile.writelines(col1 + '|' + col2 + '|' + col3)
                    prevcol3 = col3        

            d=[]
            with open('outfile.000','r',encoding="ISO-8859-1") as infile:
                fno += 1
                for line in infile.readlines():
                    data = line.strip().split('|')
                    d.append(data)
            d.sort(key=itemgetter(0))                 #sort the list `d` with the 2 item(3th column) of your sublist.

            with open('outfile2.txt','w') as outfile:
                for line in d:
                    xline = ('|'.join(line)+'\n')
                    str_idx1 = int(xline.find("|"))
                    str_idx2 = int(xline.find("http://"))
                    col1 = (xline[:str_idx1])
                    col2 = (xline[str_idx1+1:str_idx2-1])
                    col3 = (xline[str_idx2:])
                    outfile.writelines(col1+'\n')
                    outfile.writelines(col2+'\n')
                    outfile.writelines(col3)

            pre, ext = os.path.splitext(filename)
            os.rename("outfile2.txt", "--" + pre[2:] + ".m3u8")

            os.remove("outfile.000")
            os.remove(filename)
            os.remove("+-" + pre[2:] + ".m3u")


    print ("---------------------------")
    print ("Total Files: " + str(fno))
    print ("---------------------------")
    print ("")



#==========================================  TESTLINKS FUNCTION  ==========================================
def testlinks_function():

    import vlc
    import time
    import urllib
    import urllib.request
    import validators
    import socket

    socket.setdefaulttimeout(3)

    from multiprocessing import TimeoutError

    fno = 0
    totValid = 0
    totDead = 0
    
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~  BEGIN PROCESS: " + "(testlinks_function) ~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    for filename in sorted(os.listdir(path)):
    
        if filename.endswith(".m3u") or filename.endswith(".m3u8"):
        
            fno += 1
#            print ("----------  PROCESSING FILE: " + filename + "  -------------")

            with open(filename, 'r',encoding="ISO-8859-1") as searchfile:
        
                xOK = 0
                xDead = 0
                xLineCntr = 0
            
                for line in searchfile:                        

                    if 'http://blank' in line:
                        continue

                    if 'http://' in line:
                    
                        try:
                
                            xLineCntr += 1
                            if xLineCntr > 5:
                                break
                
                            url = line
                            if not validators.url(url):
                                print ("not valid")

                            code = urllib.request.urlopen(url).getcode()

                            if str(code).startswith('2') or str(code).startswith('3'):
#                                print("ok: " + url.rstrip('\r\n'))
                                xOK += 1
                            else:
#                                print("dead1: " + url.rstrip('\r\n'))
                                xDead += 1


                        except urllib.error.URLError as e: 
                            ResponseData = ''
#                            print("dead2: " + url.rstrip('\r\n'))
                            xDead += 1

                        except ValueError: 
#                            print("dead3: " + url.rstrip('\r\n'))
                            xDead += 1
                    
    #                    except socket.error as e: ResponseData = ''
    #                    except socket.timeout as e: ResponseData = ''
    #                    except UnicodeEncodeError as e: ResponseData = ''
    #                    except http.client.BadStatusLine as e: ResponseData = ''
    #                    except http.client.IncompleteRead as e: ResponseData = ''
    #                    except urllib.error.HTTPError as e: ResponseData = ''

                        except urllib.error.HTTPError as err:
#                            print("dead4: " + url.rstrip('\r\n'))
                            xDead += 1

                        except OSError as err:
#                        except socket.error as err:
#                            print("dead5: " + url.rstrip('\r\n'))
                            xDead += 1
    #                        sock.close()
                        
    #                    except RedisError:
    #                        # clean up after any error in on_connect
    #                        self.disconnect()
    #                        raise

    #                    finally:
    #                        print ("FINALLY")
                            

                
                print ("Valid Links: " + str(xOK) + ", Dead Links: " + str(xDead) + "  File: " + filename)
 
            
                if xOK == 0:
                    totValid += 1
                    copyfile(filename, path + '/Dead/' + filename)
                    os.remove(filename)
                else:
                    totDead += 1
                    copyfile(filename, path + '/Backup/' + filename)
                    

                searchfile.close


    print ("-------------------------------------------------------")
    print ("Total Files: " + str(fno) + "  Total Valid: " + str(totValid) + "  Total Dead: " + str(totDead))
    print ("-------------------------------------------------------")



#==========================================  CONCATFILES1 FUNCTION  ==========================================
def concatFiles1_function():

    fno = 0

    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~  BEGIN PROCESS: " + "(concatFiles1_function) ~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    for filename in sorted(os.listdir(path)):
    
        if filename.endswith(".m3u") or filename.endswith(".m3u8"):
        
            line1 = ""
            line2 = ""
            line3 = ""

            fno += 1
            with open(filename, 'r',encoding="ISO-8859-1") as searchfile:


                tempfile = open("temp.txt","w")
                tempfile.writelines ("\n")
                tempfile.writelines ("\n")
                tempfile.writelines("#EXTINF:0," + "**********(" + filename[2:8] + ")********\n")
                tempfile.writelines("#EXTGRP:FOOTBALL\n")
                tempfile.writelines("http://blank" + "\n")


                for line in searchfile:                        

                    if '#EXTINF:'.casefold() in line.casefold():
                        line1 = line.rstrip()
                        continue

                    if '#EXTGRP:'.casefold() in line.casefold():
                        line2 = line.rstrip()
                        continue

                    if 'http://'.casefold() in line.casefold():
                        line3 = line.rstrip()
                        tempfile.writelines(line1 + "\n")
                        tempfile.writelines(line2 + "\n")
                        tempfile.writelines(line3 + "\n")
                        line1 = ""
                        line2 = ""
                        line3 = ""
        
                tempfile.close
                searchfile.close
                print ("file = " + filename)
             

            pre, ext = os.path.splitext(filename)
            os.rename("temp.txt", pre[2:] + ".m3u8")
            os.remove(filename)


    tempfile.close()
    print ("---------------------------")
    print ("Total Files: " + str(fno))
    print ("---------------------------")
    print ("")




#==========================================  CONCATFILES2 FUNCTION  ==========================================
def concatFiles2_function():

    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~  BEGIN PROCESS: " + "(concatFiles2_function) ~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    files = os.listdir(path)
    if '.DS_Store' in files:
        files.remove('.DS_Store')
    for idx, infile in enumerate(files):
        if infile != "Dead":
            if infile !="Backup":
                print ("File to merge: " + infile)
    concat = ''.join([open(path + "/" + f,encoding="ISO-8859-1").read() for f in files if f.endswith('.m3u8')])

    with open("output" + ".m3u", "w") as fo:
        fo.write(concat)

    print ("")





#==========================================  MERGE4HOMETV FUNCTION  ==========================================
def merge4HomeTV_function(xRun):

    check = str(input("Run 4HomeTV Merge ? (Y/N): [default:N] \n")).lower().strip()
    if len(check) == 0 :
        check = "n"
    try:
        if check[0] == 'y':
            print ("Running 4HomeTV Merge!")   #return True
        elif check[0] == 'n':
#            return False
            os.remove("output.m3u")
            return check[0]
        else:
            print('Invalid Input')
            return merge4HomeTV_function(xRun)
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return merge4HomeTV_function()

    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~  BEGIN PROCESS: " + "(merge4HomeTV_function) ~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


    playlistpath = "/Users/henryvalevich/odrive/DOWNLOADS_Box_25G_valevich@aol.com/Downloads/IPTV/Playlists/4hometv10/"
    sourcepath = "/Users/henryvalevich/odrive/DOWNLOADS_Box_25G_valevich@aol.com/Downloads/IPTV/Playlists/4hometv10/Edem Source/"
    backuppath = "/Users/henryvalevich/odrive/DOWNLOADS_Box_25G_valevich@aol.com/Downloads/IPTV/Playlists/4hometv10/Backup/"

    concat2 = open("output.m3u").read()

    for filename in sorted(os.listdir(sourcepath)):
    
        if filename.endswith(".m3u") or filename.endswith(".m3u8"):
        
            print ("----------  PROCESSING FILE: " + filename + "  -------------")
            with open(sourcepath + filename, 'r',encoding="ISO-8859-1") as searchfile:
        
                concat = open(sourcepath + filename).read()
                with open(playlistpath + filename, "w") as fo:
                    fo.write(concat + concat2)
            
                str_idx = int(filename.find("."))
                newname = (filename[:str_idx] + "_" + date_time + ".m3u")
                copyfile(playlistpath + filename, backuppath + newname)

    os.remove("output.m3u")

    print ("")


#==========================================  UPDATEGDRIVE FUNCTION  ==========================================
def updateGDrive_function():

    check = str(input("Update Google Drive? (Y/N): ")).lower().strip()
    try:
        if check[0] == 'y':
            print ("Updating Google Drive!")   #return True
        elif check[0] == 'n':
            return False
        else:
            print('Invalid Input')
            return updateGDrive_function()
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return updateGDrive_function()

    
    update_main()


    print ("")




#==========================================  MAIN LOGIC  ==========================================

if __name__ == "__main__":
    
    rename_function()     

    sports_function()     

    dupesmerge_function()     

    dupesremove1_function()

    dupesremove2_function()

    testlinks_function()     

    concatFiles1_function()

    concatFiles2_function()

#    xRun = "n"
#    merge4HomeTV_function(xRun)
    
#    print ("Run GDrive Update: " + xRun)
#    if xRun.casefold() == "y":
#        updateGDrive_function()
    
    
    