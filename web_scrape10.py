import requests
import urllib.request
from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
import re

os.system('clear')
print ("=================================================================")
print ("================  DOWNLOAD FROM: dailyiptvm3u.com ===============")
print ("=================================================================")

now = datetime.now() # current date and time
#date_time = now.strftime("%m%d%Y")
ddmmyy = now.strftime("%d-%m-%Y")    
ddmmyy2 = (now + timedelta(days=-1)).strftime("%d-%m-%Y")
date_time = now.strftime("%d-%m")
print ("Today: " + ddmmyy)
print ("Yesterday: " + ddmmyy2)
path = "/users/henryvalevich/Downloads/Temp"
retval = os.getcwd()
print ("Current working directory %s" % retval)
os.chdir( path )
retval = os.getcwd()
print ("Directory changed successfully %s" % retval)

found = False

def download_function(url):

    print ("----------------------- Processing URL ------------------------------")
    print (url)

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
    down_list = soup.find(class_='download-attachments')
#    down_list_items = down_list.find_all('a')                            # Pull all text from the BodyText div

    if not down_list:
       print ("Error: URL and Items not Found! Continue...")
       return
        
    down_list_items = down_list.find_all('a')                            # Pull all text from the BodyText div
    x = 0
    for down in down_list_items:
        names = down.contents[0]
        names = names.replace("Download ","")
        links = down.get('href')
#        print(names)
#        print(links)

        r = requests.get(links)
        
        with open(names + '.m3u', 'wb') as outfile:
            

            if names[0:2] == "uk" or names[0:2] == "us":
                indate = datetime.strptime(names[3:9], "%d%m%y")
                yestdate = datetime.strptime(ddmmyy2, "%d-%m-%Y")
                if indate < yestdate: 
                    print ("Older Date: " + names[3:9] + " Skipping!")
                    os.remove(names + '.m3u')                
                    continue

            if check(names):
                print ("Already Downloaded (" + names + ")...Exiting!")
                os.remove(names + '.m3u')                
                continue

            print ("Downloading..." + names + '.m3u')                
            outfile.write(r.content)            
            f = open("/Users/henryvalevich/Downloads/-Run Scripts/m3u_downloads.txt", "a")
            mystr2 = names + "_" + links
            f.write("web_scrape10," + str(now.strftime("%m/%d/%Y-%H:%M:%S")) + "," + mystr2 + '\n')
            x += 1

    print ("---------------------------------------------------------------------")

        
    print ("--Total Files Downloaded: " + str(x))
        








def download_function2(url):

    print ("----------------------- Processing URL ------------------------------")
    print (url)

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
    down_list = soup.find(class_='download-attachments')
#    down_list_items = down_list.find_all('a')                            # Pull all text from the BodyText div

    if not down_list:
       print ("Error: URL and Items not Found! Continue...")
       return
        
    from operator import itemgetter
    d=[]

    down_list_items = down_list.find_all('a')                            # Pull all text from the BodyText div
    for down in down_list_items:
        names = down.contents[0]
        names = names.replace("Download ","")
        links = down.get('href')
        data1 = names[3:9] + "|" + names + "|" + links
        data = data1.strip().split('|')
        d.append(data)
#    d.sort(reverse=True,key=itemgetter(0))
        print (data[:6])
    d.sort(key = lambda date: datetime(data[:6],'%d%m%y'))



    x = 0
    for line in sorted(d,reverse=True,key=itemgetter(0)):
        print (line)
        xline = (','.join(line)+'\n')
        xline = xline[7:]
        print (xline)
        str_idx1 = int(xline.find(","))
        str_idx2 = int(xline.find("http://"))
        names = (xline[:str_idx1])            
        links = (xline[str_idx1+1:])
        print ("-----"+str(names[3:9]))
        print (names)
        print (links)

        r = requests.get(links)      
        with open(names + '.m3u', 'wb') as outfile:
            
            if names[0:2] == "uk" or names[0:2] == "us":
                indate = datetime.strptime(names[3:9], "%d%m%y")
                yestdate = datetime.strptime(ddmmyy2, "%d-%m-%Y")
                if indate < yestdate: 
                    print ("Older Date: " + names[3:9] + " Skipping!")
                    os.remove(names + '.m3u')                
                    continue

            if check(names):
                print ("Already Downloaded (" + names + ")...Exiting!")
                os.remove(names + '.m3u')                
                continue

            print ("Downloading..." + names + '.m3u')                
            outfile.write(r.content)            
            f = open("/Users/henryvalevich/Downloads/-Run Scripts/m3u_downloads.txt", "a")
            mystr2 = names + "_" + links
            f.write("web_scrape10," + str(now.strftime("%m/%d/%Y-%H:%M:%S")) + "," + mystr2 + '\n')
            x += 1


    print ("---------------------------------------------------------------------")
    print ("--Total Files Downloaded: " + str(x))
        




def check(txt):

    with open("/Users/henryvalevich/Downloads/-Run Scripts/m3u_downloads.txt") as dataf:
        return any(txt in line for line in dataf)


#==========================================  MAIN LOGIC  ==========================================

if __name__ == "__main__":
    
    
#    url = "https://dailyiptvm3u.com/iptv-m3u-playlist-daily-updates-iptv-links-06-03-2020/"
    url = "https://dailyiptvm3u.com/iptv-m3u-playlist-daily-updates-iptv-links-" + ddmmyy + "/"
    download_function(url)     

    url = "https://dailyiptvm3u.com/free-iptv-usa-m3u-playlist-download/"
    download_function(url)     

    url = "https://dailyiptvm3u.com/iptv-list-free-uk-m3u-playlist-updates/"
    download_function(url)     


