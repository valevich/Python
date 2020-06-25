import requests
import urllib.request
from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from datetime import datetime
import os
import re

os.system('clear')
print ("=================================================================")
print ("===========  DOWNLOAD FROM: https://en.tousecurity.com  =========")
print ("=================================================================")

now = datetime.now() # current date and time
#date_time = now.strftime("%m%d%Y")
date_time = now.strftime("%d-%m")
ddmmyy = now.strftime("%d-%m-%Y")    
print ("Today: " + ddmmyy)
path = "/users/henryvalevich/Downloads/Temp"
retval = os.getcwd()
print ("Current working directory %s" % retval)
os.chdir( path )
retval = os.getcwd()
print ("Directory changed successfully %s" % retval)

found = False

def download_function(url):

#    url = "https://en.tousecurity.com/free-iptv-links-usa/"
#    url = "https://en.tousecurity.com/iptv-free-uk/"

    print ("Processing URL: " + url)


    try:
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers={'User-Agent':user_agent,} 
        request=urllib.request.Request(url,None,headers) #The assembled request
        response = urllib.request.urlopen(request)
        data = response.read() # The data u need
    except HTTPError as err:
       if err.code == 404:
           print ("Error: URL not Found! Continue...")
           return
       else:
           raise    


    soup = BeautifulSoup(data, 'html.parser')
    artist_name_list = soup.find(class_='download-attachments')     # Pull all text from the BodyText div
    artist_name_list_items = artist_name_list.find_all('a')     # Pull text from all instances of <a> tag within BodyText div
    
    f = open("/Users/henryvalevich/Downloads/-Run Scripts/m3u_downloads.txt", "a")
    x = 0
    for artist_name in artist_name_list_items:
        names = artist_name.contents[0]
        links = artist_name.get('href')
#        print(names)
#        print(links)

        date_strings = re.findall("(\d+\-\w+)", names)
        for i in date_strings:
            if date_time <= i:
                if check(links):
                    print ("Already Downloaded..." + names + "...Exiting!")
                    continue
                x += 1
                print("Downloading..." + names)
                r = requests.get(links)
                with open(names + '.m3u', 'wb') as outfile:
                    outfile.write(r.content)
                mystr2 = names + "_" + links
                f.write("web_scrape7 ," + str(now.strftime("%m/%d/%Y-%H:%M:%S")) + "," + mystr2 + '\n')




    print ("--Total Files Downloaded: " + str(x))
    f.close()



def check(txt):
    with open("/Users/henryvalevich/Downloads/-Run Scripts/m3u_downloads.txt") as dataf:
        return any(txt in line for line in dataf)




#==========================================  MAIN LOGIC  ==========================================

if __name__ == "__main__":
    
    xDate = ddmmyy[0:2]+"-"+ddmmyy[3:5]+"-20"+ddmmyy[6:8]
#    url = "https://en.tousecurity.com/free-iptv-links-sport-m3u-list-" + ddmmyy + "/amp/"
#    url = "https://en.tousecurity.com/free-iptv-sport-m3u-list-" + xDate + "/amp/"
#    url = "https://en.tousecurity.com/free-iptv-sport-m3u-list-28-02-2020/amp/"
#    url = "https://en.tousecurity.com/m3u-list-free-iptv-sport-" + xDate + "/"
#    url = "https://en.tousecurity.com/sport-free-iptv-m3u-list-" + xDate + "/"
    url = "https://en.tousecurity.com/free-iptv-m3u-playlist-sport-" + xDate + "/"
    download_function(url)     

#    url = "https://en.tousecurity.com/free-iptv-links-usa-" + ddmmyy + "/amp/"
#    url = "https://en.tousecurity.com/free-iptv-usa-28-02-2020/amp/"
    url = "https://en.tousecurity.com/free-iptv-usa-" + xDate + "/"
    download_function(url)     

#    url = "https://en.tousecurity.com/iptv-free-uk-" + ddmmyy + "/amp/"
#    url = "https://en.tousecurity.com/iptv-free-uk-28-02-2020/amp/"
    url = "https://en.tousecurity.com/iptv-free-uk-" + xDate + "/"
    download_function(url)     




