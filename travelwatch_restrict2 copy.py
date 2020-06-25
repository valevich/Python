import os
from datetime import datetime
import requests
import json
from collections import OrderedDict
import csv
from bs4 import BeautifulSoup
import operator



print ("=====================  START  =====================")
now = datetime.now() # current date and time
date_time = now.strftime("%m%d%Y")
path = "/users/henryvalevich/Downloads/Json/"
retval = os.getcwd()
print ("Current working directory %s" % retval)
os.chdir( path )
retval = os.getcwd()
print ("Directory changed successfully %s" % retval)




#==========================================  READ FUNCTION 1 ==========================================
#
#           1. read-source:https://www.iatatravelcentre.com/international-travel-document-news/1580226297.htm
#           2. Extract text to restrictions_temp1.txt which will be used as input in next step    
#
#======================================================================================================
def read_function1():
    
    page = requests.get('https://www.iatatravelcentre.com/international-travel-document-news/1580226297.htm')
    soup = BeautifulSoup(page.text, 'html.parser')
    tempfile = open("restrictions_temp1.txt","w")
    titleList = soup.findAll('title')
    divList = soup.findAll('div', attrs={ "class" : "container"})
    tempfile.writelines(str(divList))
    tempfile.close()
    print ("Step 1: restrictions_temp1.txt created")
    print (divList)
    
    
#==========================================  READ FUNCTION 2 ==========================================
#
#           2. Reformat and create output restrictions_temp2.txt  
#
#======================================================================================================
def read_function2():
    
    line1 = ""
    line2 = ""
    line3 = ""
    xCode = ""
    DataStart = "N"
    tempfile = open("restrictions_temp2.txt","w")        


    with open('restrictions_temp1.txt', 'r') as searchfile:

        for line in searchfile:

            line = line.replace("\\", "") 
            line = line.strip()
            line = line.rstrip('\r\n')
            line = line.replace('"', '')            
            
            if DataStart == "N":
                if 'values:{' in line:
                    DataStart = "Y"
                continue
                
            line = line.replace('QR', '')
            if 'QR' in line:
                print (line)
 
            if '{' in line:
                if 'ZW:' in line:
                    DataStart = "End"
                    
                xCode =  line[0:2]
                line1 = xCode + " - \"code\":\"" + line[0:2] + "\"" + ","
                continue
                
            if 'gdp:' in line:
                line2 = line.replace('<br/><br/>', '  ')
                line2 = line2.replace('<br/>', ' ')
                line2 = line2.replace("&#32;", " ")
                line2 = xCode + " - \"description\":\"" + line2[6:] + "\""

            if '}' in line:
                if DataStart == "End":
                    tempfile.writelines(line1 + "\n")
                    tempfile.writelines(line2 + "\n")
                    # tempfile.writelines('  }\n]\n')
                    break
                else:
                    # line3 = xline + "\n"
                    tempfile.writelines(line1 + "\n")
                    tempfile.writelines(line2 + "\n")
                    # tempfile.writelines(line3)


    tempfile.close()
                    
    print ("Step 2: restrictions_temp2.txt created")

    
#==========================================  READ FUNCTION 3 ==========================================
#
#           1. read-source:https://www.travel-advisory.info/api'
#           2. Reformat and create output traveladvisories_temp2.txt  
#
#======================================================================================================  
def read_function3():
    
    response = requests.get('https://www.travel-advisory.info/api')
    with open('traveladvisories_temp1.txt', mode = 'wb') as file:
        file.write(response.content)
    
    obj = None
    with open('traveladvisories_temp1.txt') as f:
        obj = json.load(f)
    outfile = open('traveladvisories_temp1.txt', "w")
    outfile.write(json.dumps(obj, indent=4, sort_keys=True))
    outfile.close()
                    
    xscore = ''
    xrisklevel = ''
    line1 = ""
    line2 = ""
    line3 = ""
    line4 = ""
    line5 = ""
    line6 = ""    
    tempfile = open("traveladvisories_temp2.txt","w")        


    with open('traveladvisories_temp1.txt', 'r') as searchfile:

        tempfile.writelines('{\n')
        tempfile.writelines('  \"results\": [\n')
        tempfile.writelines('    {\n')

        for line in searchfile:

            if 'score' in line:
                left = "score\": "
                right = ','
                xscore = (line[line.index(left)+len(left):line.index(right)])
                if float(xscore) == 0:
                    xrisklevel = "Information not available"
                elif float(xscore) < 2.5:
                    xrisklevel = "Low Risk"
                elif float(xscore) < 3.5:
                    xrisklevel = "Medium Risk"
                elif float(xscore) < 4.5:
                    xrisklevel = "High Risk"
                elif float(xscore) < 5:
                    xrisklevel = "Extreme Warning"
                xscore = ("      \"score\": " + "\"" + xscore + " (" + xrisklevel + ")\",\n")
                # print (xscore)
                
                # line1 = line
                line1 = (xscore)
                continue
                
            if 'updated' in line:
                line2 = line.rstrip('\r\n') + ',\n'
                continue
                
            if 'continent' in line:
                line3 = line
                continue
                
            if 'iso_alpha2' in line:
                line4 = line
                continue
                
            if 'name' in line:
                if 'source' not in line:                    
                    if 'Zimbabwe' in line:
                        line5 = line
                        line6 = "      }\n      ]\n}\n"
                        tempfile.writelines(line1)
                        tempfile.writelines(line2)
                        tempfile.writelines(line3)
                        tempfile.writelines(line4)
                        tempfile.writelines(line5)
                        tempfile.writelines(line6)
                    else:
                        line5 = line
                        line6 = "      },\n      {"
                        tempfile.writelines(line1)
                        tempfile.writelines(line2)
                        tempfile.writelines(line3)
                        tempfile.writelines(line4)
                        tempfile.writelines(line5)
                        tempfile.writelines(line6)
                

    tempfile.close()
    
    
    obj = None
    with open('traveladvisories_temp2.txt') as f:
        obj = json.load(f)
    outfile = open('traveladvisories_temp2.txt', "w")
    outfile.write(json.dumps(obj, indent=4, sort_keys=True))
    outfile.close()
    
    print ("Step 3: traveladvisories_temp2.txt created")


#==========================================  READ FUNCTION 4 ==========================================
#
#           1. Reformat and create output traveladvisories_temp3.txt  
#
#======================================================================================================

def read_function4():                    

    line1 = ""
    line2 = ""
    line3 = ""
    line4 = ""
    line5 = ""
    xLine = ""    
    xCode = ""
    tempfile = open("traveladvisories_temp3.txt","w")        


    with open('traveladvisories_temp2.txt', 'r') as searchfile:

        for line in searchfile:

            xLine = line.strip()
            
            if 'iso_alpha2' in line:
                xCode =  line[27:29]
                line1 = xLine + "\n"
                continue
                
            if 'continent' in xLine:
                line2 = xLine + "\n"
                continue

            if 'name' in xLine:
                line3 = xLine + "\n"
                continue

            if 'score' in xLine:
                line4 = xLine + "\n"
                continue

            if 'updated' in xLine:
                line5 = xLine + "," + "\n"
                tempfile.writelines(xCode + " - " + line1)
                tempfile.writelines(xCode + " - " + line2)
                tempfile.writelines(xCode + " - " + line3)
                tempfile.writelines(xCode + " - " + line4)
                tempfile.writelines(xCode + " - " + line5)
                

    tempfile.close()
    
    print ("Step 4: traveladvisories_temp3.txt created")



#==========================================  READ FUNCTION 5 ==========================================
#
#           1. Merge 2 input files, Sort and Create output restrictionsadvisories_temp1.txt  
#
#======================================================================================================
def read_function5():                    

    filenames = ['restrictions_temp2.txt', 'traveladvisories_temp3.txt' ]
    with open('restrictionsadvisories_tempx.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                outfile.write(infile.read())

    tempfile = open("restrictionsadvisories_temp1.txt","w")        
    with open('restrictionsadvisories_tempx.txt', 'r') as f:
        sorted_lines = sorted(f, key=operator.itemgetter(slice(0, 24)))
    tempfile.writelines(sorted_lines)
    os.remove("restrictionsadvisories_tempx.txt")

    print ("Step 5: restrictionsadvisories_temp1.txt created")



#==========================================  READ FUNCTION 6 ==========================================
#
#           1. Reformat and create JSON output restrictionsadvisories_temp2.txt  
#
#======================================================================================================
def read_function6():                    

    line0 = ""
    line1 = ""
    line2 = ""
    line3 = ""
    line4 = ""
    line5 = ""
    line6 = ""
    xlineno = 0
    xlinecode = ""
    xprevcode = ""
    
    tempfile = open("restrictionsadvisories.json","w")        


    with open('restrictionsadvisories_temp1.txt', 'r') as searchfile:

        tempfile.writelines('[\n')
        tempfile.writelines('  {\n')
        

        for line in searchfile:
            
            if 'code\":' in line:
                xlinecode = line[0:4]
                if xprevcode != xlinecode:
                    xprevcode = xlinecode
                    if xlineno > 0:
                        tempfile.writelines("    " + line0[5:])
                        tempfile.writelines("    " + line1[5:])
                        tempfile.writelines("    " + line2[5:])
                        tempfile.writelines("    " + line3[5:])
                        tempfile.writelines("    " + line4[5:])
                        tempfile.writelines("    " + line5[5:]) 
                        tempfile.writelines("    " + line6[5:])
                        tempfile.writelines('  },\n')
                        tempfile.writelines('  {\n')
                        
                    xlineno = xlineno + 1                    
                line0 = line
                continue
                
            if 'iso_alpha2\":' in line:
                line1 = line
                continue
                
            if 'continent\":' in line:
                line2 = line
                continue

            if 'name\":' in line:
                line3 = line
                continue

            if 'score\":' in line:
                line4 = line
                continue

            if 'updated\":' in line:
                line5 = line
                # line5 = str(line5) + ",\n"
                
            if 'description\":' in line:
                line = line.replace("\',\"","\"")
                line6 = line
                
    tempfile.writelines("    " + line0[5:])
    tempfile.writelines("    " + line1[5:])
    tempfile.writelines("    " + line2[5:])
    tempfile.writelines("    " + line3[5:])
    tempfile.writelines("    " + line4[5:])
    tempfile.writelines("    " + line5[5:])
    tempfile.writelines("    " + line6[5:])
    tempfile.writelines('  }\n')
    tempfile.writelines(']')
    xlineno = xlineno + 1                    

    tempfile.close()
  
    print ("Step 6: restrictionsadvisories.json created")
    print ("Step 6: total lines written: " + str(xlineno))



    # os.remove("restrictions_temp1.txt")
    # os.remove("restrictions_temp2.txt")
    # os.remove("traveladvisories_temp1.txt")
    # os.remove("traveladvisories_temp2.txt")
    # os.remove("traveladvisories_temp3.txt")
    # os.remove("restrictionsadvisories_temp1.txt")



#==========================================  MAIN ==========================================
#
#======================================================================================================

if __name__ == "__main__":

    read_function1()
    read_function2()
    read_function3()
    read_function4()
    read_function5()
    read_function6()
    
    

                    