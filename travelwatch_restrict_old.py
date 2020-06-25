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
#           1. read-source:https://www.iatatravelcentre.com/international-travel-document-news/1580226297.htm
#           2. Extract text to restrict.txt which will be used as input in next step    
#
#======================================================================================================
def read_function1():
    
    page = requests.get('https://www.iatatravelcentre.com/international-travel-document-news/1580226297.htm')
    soup = BeautifulSoup(page.text, 'html.parser')
    tempfile = open("restrict.txt","w")
    titleList = soup.findAll('title')
    divList = soup.findAll('div', attrs={ "class" : "middle"})
    tempfile.writelines(str(divList))
    tempfile.close()
    print ("Step 1 Done: restrict.txt created")
    
    
    
#==========================================  READ FUNCTION 2 ==========================================
#
#   Ignore (replaced by read_function0) -> 1. view-source:https://www.iatatravelcentre.com/international-travel-document-news/1580226297.htm
#   Ignore (replaced by read_function0) -> 2. Copy and Paste text to restrict.txt which will be used as input in this step    
#           3. Run this step to create restrict.js file
#           4. Delete Data from Firebase
#           5. Run in terminal command--> 'node restrict.js' to upload file to Firebase  
#
#======================================================================================================
def read_function2():
    
    line1 = ""
    line2 = ""
    line3 = ""
    DataStart = "N"
    tempfile = open("restrict.js","w")        


    with open('restrict.txt', 'r') as searchfile:

        tempfile.writelines('const firebase = require("firebase");\n')
        tempfile.writelines('require("firebase/firestore");\n')
        tempfile.writelines('firebase.initializeApp({\n')
        # tempfile.writelines('    apiKey: "AIzaSyBT_dpAPy--UYnnv3n9QyemUNULE635Rvg",\n')
        # tempfile.writelines('    authDomain: "valevaweb.firebaseapp.com",\n')
        # tempfile.writelines('    projectId: "valevaweb"\n')
        tempfile.writelines('    apiKey: "AIzaSyAuL_HiM4nF-DoIrD8Af-Mh51BKoZO1eng",\n')
        tempfile.writelines('    authDomain: "travelwatch-f51c7.firebaseapp.com",\n')
        tempfile.writelines('    projectId: "travelwatch-f51c7"\n')
        tempfile.writelines('  });\n')
        tempfile.writelines('var db = firebase.firestore();\n\n')
        tempfile.writelines('var menu =[\n')


        for line in searchfile:

            if DataStart == "N":
                if 'values:{' in line:
                    DataStart = "Y"
                continue
 
            if '{' in line:
                if 'ZW:' in line:
                    DataStart = "End"
                    
                    
                line = line.strip()
                # line = line[1:]
                line1 = "{\n" + "   \"code\":\"" + line[0:2] + "\"" + "," + "\n"
                continue
                
            if 'gdp:' in line:
                line = line.rstrip('\r\n')
                line = line.replace('"', '')
                line2 = line.replace('<br/><br/>', '  ')
                line2 = line2.replace('<br/>', ' ')
                line2 = line2.replace("&#32;", " ")
                line2 = "   \"description\":\"" + line2[6:] + "\""

            if '}' in line:
                if DataStart == "End":
                    tempfile.writelines(line1)
                    tempfile.writelines(line2)
                    tempfile.writelines('  }\n]\n')
                    break
                else:
                    line3 = line
                    tempfile.writelines(line1)
                    tempfile.writelines(line2)
                    tempfile.writelines(line3)


        # tempfile.writelines(']\n')
        tempfile.writelines('menu.forEach(function(obj) {\n')
        tempfile.writelines('    db.collection("restrictions").add({\n')
        tempfile.writelines('        code: obj.code,\n')
        tempfile.writelines('        description: obj.description,\n')
        tempfile.writelines('    }).then(function(docRef) {\n')
        tempfile.writelines('        console.log("Document written with ID: ", docRef.id);\n')
        tempfile.writelines('    })\n')
        tempfile.writelines('    .catch(function(error) {\n')
        tempfile.writelines('        console.error("Error adding document: ", error);\n')
        tempfile.writelines('    });\n')
        tempfile.writelines('});\n')



    tempfile.close()
                    
    print ("Step 2 Done: restrict.js created")





if __name__ == "__main__":

    read_function1()
    read_function2() 
    

                    