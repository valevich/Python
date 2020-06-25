import requests
import urllib.request
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
from datetime import datetime
import os
import re
import zipfile, io
import shutil
import sys

os.system('clear')
print ("")
print ("=================================================================")
print ("==============  DOWNLOAD FROM: https://flylinks.net  ============")
print ("=================================================================")
now = datetime.now() # current date and time
#date_time = now.strftime("%m%d%Y")
date_time = now.strftime("%d-%m")
print ("Today: " + date_time)
path = "/users/henryvalevich/Downloads/Temp/"
retval = os.getcwd()
print ("Current working directory %s" % retval)
os.chdir( path )
retval = os.getcwd()
print ("Directory changed successfully %s" % retval)



def main_function():

    url = "https://flylinks.net/free-iptv-sport-m3u-links-2019/"
    #url = "https://flylinks.net/unlimited-iptv-world-m3u-free-download-28-08-2019/"

    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,} 
    request=urllib.request.Request(url,None,headers) #The assembled request
    response = urllib.request.urlopen(request)
    data = response.read() # The data u need


    # ========= TEST VERSION ===============
    #soup = BeautifulSoup(data, 'html.parser')
    #artist_name_list = soup.find(class_='td_btn td_btn_md td_3D_btn')       # Pull all text from the BodyText div
    #artist_name_list_items = artist_name_list.find_all('a')                 # Pull text from all instances of <a> tag within BodyText div
    #for artist_name in artist_name_list_items:
    #    names = artist_name.contents[0]
    #    links = artist_name.get('href')
    #    print(names)
    #    print(links)

    #=====  To get a list of everyhref regardless of tag use:
    #href_tags = soup.find_all(href=True)   
    #hrefs = [tag.get('href') for tag in href_tags]
    #print (hrefs)

    soup = BeautifulSoup(data, 'html.parser')
    line_list1 = (soup.find_all(class_='td_btn td_btn_md td_3D_btn')[-1])       # Pull all text from last occurance
    line_list2 = line_list1.find('a') 
    link1 = line_list2.get('href')
    #print (line_list1.contents[0])
    print (line_list2.contents[0])
    print (link1)

    if check(link1):
        print ("Already Downloaded...Exiting!")
        sys.exit()
    else:
        print ("Downloading..." + link1)

    f = open("/Users/henryvalevich/Downloads/-Run Scripts/m3u_downloads.txt", "a")
    mystr2 = line_list2.contents[0] + "_" + link1
    f.write("web_scrape8 ," + str(now.strftime("%m/%d/%Y-%H:%M:%S")) + "," + mystr2 + '\n')


    #date_string = re.findall("(\d+\-\w+\-\w+)", line_list2.contents[0])
    date_string1 = re.findall("(\d+\-\d+\-\d+)", line_list2.contents[0])
    #print (date_string1)
    date_string2 = date_string1[0]
    #print (date_string2)
    date_string3 = date_string2[6:10] + date_string2[3:5] + date_string2[0:2]
    #print (date_string3)

    # ========= DOWNLOAD ===============
    #    date_strings = re.findall("(\d+\-\w+)", names)
    #    for i in date_strings:
    #        if date_time == i:
    #            print(names)
    #            r = requests.get(links)
    #            with open(names + '.m3u', 'wb') as outfile:
    #                outfile.write(r.content)

    # ========= DOWNLOAD ===============
    #r = requests.get(link1)
    #with open('test.zip', 'wb') as outfile:
    #    outfile.write(r.content)
    
    # ========= DOWNLOAD AND EXTRACT ZIP FILE ===============
    zdir = r'/users/henryvalevich/Downloads/test/'
    r = requests.get(link1)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(zdir)


    # ========= RENAME/MOVE DIR AND SUBDIR FILES ===============
    filedate = now.strftime("%Y%m%d")
    i = 0
    for dirpath, dirnames, filenames in os.walk(zdir):
        for file in filenames:
         filepath = dirpath +os.sep+file
         if filepath.endswith('m3u') or filepath.endswith('m3u8'):
            i += 1
            new_name = date_string3 + '_flylinks.net_' + str(i) + ".m3u"
            os.rename(filepath,'/users/henryvalevich/Downloads/temp/'+os.sep+new_name)

    shutil.rmtree(zdir)

    print ("Total Files Downloaded: " + str(i))



def check(txt):

    with open("/Users/henryvalevich/Downloads/-Run Scripts/m3u_downloads.txt") as dataf:
        return any(txt in line for line in dataf)



def clean_links_function():

    print ("==============  Clean Links Function  ============")
    print ("")

    xline = ""
    toremove = ['https://flylinks.net,','https://flylinks.net, ','https://flylinks.net - ']
    
    for filename in os.listdir("/Users/henryvalevich/Downloads/Temp/"):
    
        if filename.endswith(".m3u") or filename.endswith(".m3u8"):
        
            tempfile = open("output.txt","w")
            renam = "no"
        
            with open(filename, 'r',encoding="ISO-8859-1") as searchfile:
        
                print ("----------- FILE PROCESSING " + filename + "------- ")
            
                i = 0
                for line in searchfile:
        
                    xline = line
                    if '#extinf:'.casefold() in line.casefold():
                        for item in toremove:    
                            if item.casefold() in line.casefold():
                                xline = line.replace(item,"")
                                i += 1
#                                print ("line: " + line + " Replaced: " + xline)
                            
                    tempfile.writelines(xline)                        

                searchfile.close
                os.remove(filename)
                os.rename("output.txt", (filename))
                tempfile.close()
    
    print ("Total lines Replaced: " + str(i))
    

#==========================================  MAIN LOGIC  ==========================================

if __name__ == "__main__":
    
    main_function()     

    clean_links_function()     

