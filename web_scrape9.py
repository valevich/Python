import requests
import urllib.request
from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from datetime import datetime
import os
import re
import sys
from urllib.parse import urlparse

os.system('clear')
print ("=================================================================")
print ("=========  DOWNLOAD FROM: https://www.dailym3uiptv.com  =========")
print ("=================================================================")

now = datetime.now() # current date and time
#date_time = now.strftime("%m%d%Y")
date_time = now.strftime("%d-%m")
print ("Today: " + date_time)
path = "/users/henryvalevich/Downloads/Temp"
retval = os.getcwd()
print ("Current working directory %s" % retval)
os.chdir( path )
retval = os.getcwd()
print ("Directory changed successfully %s" % retval)

found = False

def download_function(url,tagid):

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
    down_list = soup.find(id=tagid)                             # Pull all text from the BodyText div
    down_list_items = down_list.find_all('a')                   # Pull text from all instances of <a> tag within BodyText div
    
    x = 0
    for down in down_list_items:
        names = down.contents[0]
        names = names.replace("Download ","")
        links = down.get('href')
 #       print(names)

        x += 1
        r = requests.get(links)
        

        with open(names + '.m3u', 'wb') as outfile:

            myString_list = [item for item in str(r.content).split("#")]
            for item in myString_list:
                try:
                    mystr = (re.search("(?P<url>https?://[^\s]+)", item).group("url"))
                    pre, ext = os.path.splitext(mystr)
                    mystr2 = (names.replace(" ","") + "_" + pre)
#                    print (mystr2)
                    break
                except:
                    pass  
            
            if check(mystr2):
                print ("Already Downloaded (" + names + ")...Exiting!")
                os.remove(names + '.m3u')
                continue               

            print ("Downloading..." + names + '.m3u')                
            outfile.write(r.content)
            f = open("/Users/henryvalevich/Downloads/-Run Scripts/m3u_downloads.txt", "a")
            f.write("web_scrape9 ," + str(now.strftime("%m/%d/%Y-%H:%M:%S")) + "," + mystr2 + '\n')


        
    print ("--Total Files Downloaded: " + str(x))
        
        


def download_function2(url,tagid):

    print ("Processing URL: " + url)

    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,} 
    request=urllib.request.Request(url,None,headers) #The assembled request
    response = urllib.request.urlopen(request)
    data = response.read() # The data u need


    soup = BeautifulSoup(data, 'html.parser')
    link_name = ""

    urls = []
    for h in soup.find_all('b'):
        a = h.find('a')
        if not a:
            continue
        urls.append(a.attrs['href'])

    f = open("/Users/henryvalevich/Downloads/-Run Scripts/m3u_downloads.txt", "a")
    x = 0
    for link_name in urls:
        print(link_name)

        x += 1
        r = requests.get(link_name)
        outfilename = os.path.basename(link_name)
        print("Downloading..." + outfilename)
        with open(outfilename, 'wb') as outfile:
            outfile.write(r.content)


#        date_strings = re.findall("(\d+\-\w+)", names)
#        for i in date_strings:
#            if date_time <= i:
#                if check(links):
#                    print ("Already Downloaded..." + names + "...Exiting!")
#                    continue
#                x += 1
#                print("Downloading..." + names)
#                r = requests.get(links)
#                with open(names + '.m3u', 'wb') as outfile:
#                    outfile.write(r.content)
#                mystr2 = names + "_" + links
#                f.write("web_scrape7 ," + str(now.strftime("%m/%d/%Y-%H:%M:%S")) + "," + mystr2 + '\n')




    print ("--Total Files Downloaded: " + str(x))
    f.close()

       



def check(txt):

    with open("/Users/henryvalevich/Downloads/-Run Scripts/m3u_downloads.txt") as dataf:
        return any(txt in line for line in dataf)




#==========================================  MAIN LOGIC  ==========================================

if __name__ == "__main__":
    
#    url = "https://www.dailym3uiptv.com/p/get-sports-iptv-links.html"
#    tagid = "aim26903022384055098734"
#    download_function(url,tagid)     

#    url = "https://www.dailym3uiptv.com/p/get-woldwide-iptv-links.html"
#    tagid = "aim26914974246734341312"
#    download_function(url,tagid)     

#    url = "https://www.dailym3uiptv.com/p/get-usa-iptv.html"
#    tagid = "aim26881774670770946201"
#    download_function(url,tagid)     

#    url = "https://www.dailym3uiptv.com/p/get-uk-iptv-links.html"
#    tagid = "aim23100701974655500321"
#    download_function(url,tagid)     

    url = "https://www.dailym3uiptv.com/2020/02/world-iptv-m3u-download.html"
    tagid = ""
    download_function2(url,tagid)     



