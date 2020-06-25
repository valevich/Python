import os
from datetime import datetime

print ("=====================  START  =====================")
now = datetime.now() # current date and time
date_time = now.strftime("%m%d%Y")
path = "/users/henryvalevich/Downloads/Temp Sports/"
retval = os.getcwd()
print ("Current working directory %s" % retval)
os.chdir( path )
retval = os.getcwd()
print ("Directory changed successfully %s" % retval)



#==========================================  SOCCER FUNCTION  ==========================================
def soccer_function():
    
    line1 = ""
    line2 = ""

    allowed = ['NBCSN', 'NBC GOLD', 'NBC Sports', 'RUSH SPORT', ' EPL ', 'LFC TV', 'MUTV', 'CHELSEA', \
                'Sky Sports Premier League', 'Sky Sports Main Event', 'Sky Sports Football', 'Sky Sports News', \
                'BT Sport 1', 'BT Sports 1', 'BT Sport 2', 'BT Sports 2', 'BT Sport 3', 'BT Sports 3'
    #            'BEIN SPORT', 'BEINSPORT', 'Fox Soccer', 'Gol TV', 'Sky Sport Bundesliga', \
    #            'ELEVEN SPORTS',  \
                 ]
            
    tempfile = open("output.txt","w")        
    xLinks1 = 0
    xLinks2 = 0

    for filename in sorted(os.listdir(path)):
    
        if filename.endswith(".m3u") or filename.endswith(".m3u8"):
        
            with open(filename, 'r') as searchfile:
        
                print ("----------- FILE PROCESSING " + filename + "------- ")
                i = 0
                xValid = "N"
            
                for line in searchfile:
        
                    if '#EXTINF:'.casefold() in line.casefold():
                        for item in allowed:    
                            if item.casefold() in line.casefold():
                                line1 = line
                                xValid = "Y"
    #                        else:
    #                            xValid = "N"
                        continue

                    if '#EXTGRP:'.casefold() in line.casefold():
                        line2 = line
                        continue
                                
                    if 'http://'.casefold() in line.casefold():
                        xLinks1 += 1
                        if xValid == "Y":
                            tempfile.writelines(line1)
                            tempfile.writelines(line2)
                            tempfile.writelines(line)
                            xLinks2 += 1

                        xValid = "N"
                                                	

                searchfile.close

    tempfile.close()
    print ("Input Channels: " + str(xLinks1) + " ---> Sport Channels: " + str(xLinks2))
                    
         
#==========================================  DUPESREMOVE1 FUNCTION  ==========================================
def dupesremove1_function():
    
    fno = 0

    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~  BEGIN PROCESS: " + "(dupesremove1_function) ~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
    line1 = ""
    line2 = ""
    line3 = ""

    with open("output.txt", 'r',encoding="ISO-8859-1") as searchfile:

        tempfile = open("tempsort.txt","w")
        for line in searchfile:                        

            line = ''.join([s for s in line if ord(s) < 127])
            
            if '#EXTINF:'.casefold() in line.casefold():
                line1 = line.rstrip()
                continue

            if '#EXTGRP:'.casefold() in line.casefold():
                line2 = line.rstrip()
                continue

            if 'http://'.casefold() in line.casefold():
                fno += 1
                line3 = line.rstrip()
                tempfile.writelines(line1 + "|" + line2 + "|" + line3 + "\n")
                line1 = ""
                line2 = ""
                line3 = ""

        tempfile.close
        searchfile.close
     

    os.remove("output.txt")
                

    print ("---------------------------")
    print ("Total Links: " + str(fno))
    print ("---------------------------")
    print ("")



                    
                    
#==========================================  DUPESREMOVE2 FUNCTION  ==========================================
def dupesremove2_function():
    
    from operator import itemgetter

    fno = 0
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~  BEGIN PROCESS: " + "(dupesremove2_function) ~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


    prevcol3 = ""
    d=[]

    with open("tempsort.txt",'r',encoding="ISO-8859-1") as infile:
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
                if "http://blank" not in col3:
                    outfile.writelines(col1 + '|' + col2 + '|' + col3)
            prevcol3 = col3        

    d=[]
    with open('outfile.000','r',encoding="ISO-8859-1") as infile:
        for line in infile.readlines():
            data = line.strip().split('|')
            d.append(data)
#            d.sort(key=itemgetter(0))                 #sort the list `d` with the 2 item(3th column) of your sublist.

    with open('outfile2.txt','w') as outfile:
        prevcol3 = ""
        lineno = 0
        outfile.writelines(""+'\n')
        outfile.writelines("#EXTINF:0,******** SOCCER ********"+'\n')
        outfile.writelines("#EXTGRP:FOOTBALL"+'\n')
        outfile.writelines("http://blank"+'\n')

        for line in d:
            lineno += 1
            xline = ('|'.join(line)+'\n')
            str_idx1 = int(xline.find("|"))
            str_idx2 = int(xline.find("http://"))
            col1 = (xline[:str_idx1])
            col2 = (xline[str_idx1+1:str_idx2-1])
            col3 = (xline[str_idx2:])
            
            col3short = (col3.rsplit('/', 1)[0])
            if prevcol3 != col3short:
                prevcol3 = col3short
            outfile.writelines(col1+'\n')
            if not col2:
                outfile.writelines("#EXTGRP:FOOTBALL"+'\n')
            else:
                outfile.writelines(col2+'\n')
            outfile.writelines(col3)
            fno += 1
            

    os.rename("outfile2.txt", "-soccer.m3u")
    os.remove("outfile.000")
    os.remove("tempsort.txt")


    print ("---------------------------")
    print ("Total Lines: " + str(fno))
    print ("---------------------------")
    print ("")




if __name__ == "__main__":

    soccer_function()

    dupesremove1_function()

    dupesremove2_function()

                    