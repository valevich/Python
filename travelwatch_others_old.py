import os
from datetime import datetime
import requests
import json
from collections import OrderedDict
import csv
from bs4 import BeautifulSoup


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
#           1. Run this step to create traveladvisories.json file
#           2. Upload JSON file to Github 
#
#======================================================================================================
def read_function1():
    

    response = requests.get('https://www.travel-advisory.info/api')
    with open('traveladvisories_temp.json', mode = 'wb') as file:
        file.write(response.content)
    
    obj = None
    with open('traveladvisories_temp.json') as f:
        obj = json.load(f)
    outfile = open('traveladvisories_temp.json', "w")
    outfile.write(json.dumps(obj, indent=4, sort_keys=True))
    outfile.close()
                    

    line1 = ""
    line2 = ""
    line3 = ""
    line4 = ""
    line5 = ""
    line6 = ""    
    tempfile = open("traveladvisories.json","w")        


    with open('traveladvisories_temp.json', 'r') as searchfile:

        tempfile.writelines('{\n')
        tempfile.writelines('  \"results\": [\n')
        tempfile.writelines('    {\n')

        for line in searchfile:

            if 'score' in line:
                line1 = line                  # "\"score\":\"" + line[0:2] + "\"" + "," + "\n"
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
    with open('traveladvisories.json') as f:
        obj = json.load(f)
    outfile = open('traveladvisories.json', "w")
    outfile.write(json.dumps(obj, indent=4, sort_keys=True))
    outfile.close()
    
    
#==========================================  READ FUNCTION 2 ==========================================
#
#           1. Run this step to create country_tipping2.json file
#           2. Upload JSON file to Github 
#
#======================================================================================================
def read_function2():
    
    #------------------ 1. CONVERT CSV FILE TO JSON FORMAT ------------------
    data = {}
    with open('country_tipping.csv') as csvFile:
        csvReader = csv.DictReader(csvFile)
        for rows in csvReader:
            id = rows['Country']
            data[id] = rows

    # print(json.dumps(OrderedDict(sorted(data.items())), indent=4))

    #------------------ 2. REFORMAT AND SORT TO NICE JSON FORMAT ------------------
    with open('country_tipping.json', 'w') as jsonFile:
        jsonFile.write(json.dumps(OrderedDict(sorted(data.items())), indent=4))
    jsonFile.close()
    
    
    #------------------ 3. REFORMAT JSON TO MY SPECS  ------------------
    tempfile = open("country_tipping2.json","w")
    with open('country_tipping.json', 'r') as searchfile:

        tempfile.writelines('{\n')
        tempfile.writelines('  \"results\": [\n')
        tempfile.writelines('    {\n')

        for line in searchfile:

            if ': {' in line:
                continue
                
            if 'Country' in line:
                tempfile.writelines(line)
                continue
                
            if 'Taxis' in line:
                tempfile.writelines(line)
                continue
                
            if 'Porters' in line:
                tempfile.writelines(line)
                continue
                
            if 'iso_alpha2' in line:
                tempfile.writelines(line)
                continue
                
            if 'Restaurants' in line:
                tempfile.writelines(line.rstrip('\r\n') + ",\n")
                tempfile.writelines('     },\n     {\n')
                continue
    

    tempfile.close()
    





if __name__ == "__main__":

    read_function1()
#    read_function2() 
    

                    