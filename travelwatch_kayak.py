import requests
import urllib.request
from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import csv, json, requests, sys
from datetime import datetime, timedelta
import os
import re
import pprint
from collections import OrderedDict

os.system('clear')
print ("=================================================================")
print ("=                              BeautifulSoup                            ")
print ("=================================================================")

now = datetime.now() # current date and time
ddmmyy = now.strftime("%d-%m-%Y")    
print ("Today: " + ddmmyy)
path = "/users/henryvalevich/Downloads/Json"
retval = os.getcwd()
print ("Current working directory %s" % retval)
os.chdir( path )
retval = os.getcwd()
print ("Directory changed successfully %s" % retval)

found = False

#==========================================  download_function  ==========================================
def download_function(url):

    print ("----------------------- Processing URL ------------------------------")
    print (url)

    tempfile = open("kayak_temp1.txt","w")
    data = urllib.request.urlopen (url)
    soup = BeautifulSoup(data, 'html.parser')
    containers = soup.findAll(["h2", "h3", "img", "p"])
    for container in containers:
         # if 'src='.casefold() in str(container).casefold():
         #     print (container)
        tempfile.writelines(str(container)+"\n")

    tempfile.close()
    print ("---------------- Input File: kayak_temp1.txt Created -------------------")
    

#==========================================  cleanup_input  ==========================================
def cleanup_input():

    tempfile = open("kayak_temp2.txt","w") 
    
    with open('kayak_temp1.txt', 'r') as searchfile:
        
        pline = 'n'
        line2 = ''
        
        
        for line in searchfile:
                
            if '<h2' in line:
                if 'CountryGroup__title' in line:
                    tempfile.writelines(line)
                    continue
                elif 'FaqSection__title' in line:
                    continue
                elif 'AdditionalResources__title' in line:
                    continue
            
            if '<img' in line:
                pline == 'n'
                if 'CountryReport__flag' in line:
                    tempfile.writelines(line)
                    continue
            
            if '<h3' in line:
                if 'CountryReport__countryName' in line:
                    tempfile.writelines(line)
                    continue

            if 'CountryList__description' in line or 'CountryList__legal' in line:
                continue
            
            if 'CountryReport__paragraph' in line:
                pline = 'y'
                
            if pline == 'y':
                if line.strip():
                    tempfile.writelines(line)
                    continue

        tempfile.close()
        print ("--------------- Output File: kayak_temp2.txt Created -------------------")
        


#==========================================  format_json()  ==========================================
def format_json():

    tempfile = open("kayak_temp3.txt","w") 
    
    with open('kayak_temp2.txt', 'r') as searchfile:
        # tempfile.writelines('{\n')
        # tempfile.writelines('  \"results\": [\n')
        # tempfile.writelines('    {\n')

        tempfile.writelines('[\n')
        tempfile.writelines('    {\n')
        
        xLine = ''
        xLineGroup = ''
        xCountryGroup = ''
        xiso_alpha2 = ''
        xLineNo = 0
        xCountry = ''
        xReport1 = ''
        xReport2 = ''
        xCovidLine = ''
        
        for line in searchfile:
                        
            if '<h2' in line:
                if 'CountryGroup__title' in line:
                    xCountryGroup = line.partition("title\">")[2].partition("</h2>")[0]
                    xLineGroup = '      \"countrygroup\": \"' + xCountryGroup + '\",\n'
                    continue
            
            if '<img' in line:
                if 'CountryReport__flag' in line:
                    xLineNo = xLineNo + 1
                    if xLineNo > 1:
                        tempfile.writelines('    },\n')
                        tempfile.writelines('    {\n')
                    tempfile.writelines(xLineGroup)
                    xiso_alpha2 = line.partition("alt=\"")[2].partition(" flag")[0]
                    xLine = '      \"iso_alpha2\": \"' + xiso_alpha2.lower() + '\",\n'
                    tempfile.writelines(xLine)
                    xFlagURL = line.partition("src=")[2].partition("/>")[0]
                    xLine = '      \"flagurl\": ' + xFlagURL + ',\n'
                    tempfile.writelines(xLine)
                    continue

            if '<h3' in line:
                if 'CountryReport__countryName' in line:
                    xCountry = line.partition("countryName\">")[2].partition("</h3>")[0]
                    xLine = '      \"country\": \"' + xCountry + '\",\n'
                    tempfile.writelines(xLine)
                    continue

            if 'CountryReport__paragraph\">' in line:
                xReport1 = line.partition("CountryReport__paragraph\">")[2].partition("</p>")[0]
                xLine = '      \"report1\": \"' + xReport1.strip() + '\",\n'
                tempfile.writelines(xLine)
                continue

            if '<p>' in line:
                xReport2 = xReport2.strip() + line.partition("<p>")[2].partition("</p>")[0] + " "
                continue

            if 'CountryReport__paragraph--toggleable\">' in line:
                xReport2 = xReport2.replace("\"","-")
                xLine = '      \"report2\": \"' + xReport2.strip() + '\",\n'
                tempfile.writelines(xLine)
                xReport2 = ''
                continue
                
            if 'There are currently' in line:
                xLine = line.replace("</p>","")
                xCovidLine = '      \"covidcases\": \"' + xLine.strip() + '\"\n'
                tempfile.writelines(xCovidLine)
                continue


        # tempfile.writelines('    }\n')
        # tempfile.writelines('  ]\n')
        # tempfile.writelines('}')

        tempfile.writelines('    }\n')
        tempfile.writelines(']\n')
        
        tempfile.close()
        
        print ("--------------- Output File: kayak_temp3.txt Created -------------------")
        print ("Countries Processed: " + str(xLineNo))
        
        

#=======================  format_json2()  remove trailing commas on last data line which cause an error =====================
def format_json2():

    tempfile = open("kayak_temp4.txt","w") 
    
    with open('kayak_temp3.txt', 'r') as searchfile:
        
        xLine = ''
        xPrevLine = ''
        
        for line in searchfile:
                
            if '},' in line:
                if '\",' in xPrevLine:
                    xPrevLine = xPrevLine.replace("\",","\"")

            tempfile.writelines(xPrevLine)
            xPrevLine = line

        tempfile.writelines(xPrevLine)

        
        tempfile.close()
        
        print ("--------------- Output File: kayak_temp4.txt Created -------------------")
        



#==========================================  sort_json()  ==========================================
def sort_json():

    # #------------------ 2. REFORMAT AND SORT TO NICE JSON FORMAT ------------------
    
    obj = None
    with open('kayak_temp4.txt') as f:
        obj = json.load(f)

    def country(d):
        return d['country']
    
    obj2 = sorted(obj, key=country)

    with open('kayak_restrictions.json', 'w') as outfile:
         json.dump(obj2, outfile, sort_keys = True, indent = 4,
                   ensure_ascii = False)

    print ("--------------- Output File: kayak_restrictions.json Created -------------------")


    os.remove("kayak_temp1.txt")
    os.remove("kayak_temp2.txt")
    os.remove("kayak_temp3.txt")
    os.remove("kayak_temp4.txt")
    


#==========================================  MAIN LOGIC  ==========================================

if __name__ == "__main__":
    
    
    url = "https://www.kayak.com/travel-restrictions"
    
    download_function(url)
    cleanup_input()
    format_json()
    format_json2()
    sort_json()


