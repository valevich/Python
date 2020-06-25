import os
import sys
import vlc
import time
import urllib
import urllib.request
import validators
import socket
from shutil import copyfile
socket.setdefaulttimeout(3)
from multiprocessing import TimeoutError
from datetime import datetime

os.system('clear')


#==========================================  CONCATFILES1 FUNCTION  ==========================================
def concatFiles1_function(path):

    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~  BEGIN PROCESS: " + "(concatFiles1_function) ~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    now = datetime.now() # current date and time
    date_time = now.strftime("%m%d%Y")
    retval = os.getcwd()
    print ("Current working directory %s" % retval)
    os.chdir( path )
    retval = os.getcwd()
    print ("Directory changed successfully %s" % retval)

    fno = 0

    print ("---------------------------------------------------")
    for filename in sorted(os.listdir(path)):
    
        if filename.endswith(".m3u") or filename.endswith(".m3u8"):
        
            fno += 1
            with open(filename, 'r') as searchfile:
        
                xOK = 0
                xDead = 0
                xLineCntr = 0
            
                for line in searchfile:                        

                    if 'http://' in line:
                    
                        if 'http://blank' in line:
                            continue
                    
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
#                            print("dead5: " + url.rstrip('\r\n'))
                            xDead += 1
    #                        sock.close()
                        
    #                    except RedisError:
    #                        # clean up after any error in on_connect
    #                        self.disconnect()
    #                        raise

    #                    finally:
    #                        print ("FINALLY")
                            

                
                print ("Valid Links: " + str(xOK) + "/" + str(xDead) + " -- " + filename )
#                print ("---------------------------------------------------")
            
                if xOK == 0:
                    copyfile(filename, path + 'Dead/' + filename)
                    os.remove(filename)

                if xOK == 5:
                    if filename[0:1] != "-":
                        os.rename(filename, '-' + filename)


                searchfile.close


    print ("---------------------------------------------------")
    print ("Total Files: " + str(fno))
    print ("---------------------------------------------------")



#==========================================  CONCATFILES2 FUNCTION  ==========================================
def concatFiles2_function(xpath):

    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~  BEGIN PROCESS: " + "(concatFiles2_function) ~~~~~~~~~~~~~~")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    path = xpath
    files = os.listdir(path)
    if '.DS_Store' in files:
        files.remove('.DS_Store')
    for idx, infile in enumerate(files):
        if infile != "Dead":
            if infile !="Backup":
                print ("File to merge: " + infile)
    concat = ''.join([open(path + "/" + f,encoding="ISO-8859-1").read() for f in files if f.endswith('.m3u') or f.endswith('.m3u8')])

    with open("output" + ".m3u", "w") as fo:
        fo.write(concat)

    print ("")




#==========================================  MAIN LOGIC  ==========================================

if __name__ == "__main__":

    
#    path = str(input("Enter Path: [default:/Users/henryvalevich/Downloads/Temp Current] \n")).lower().strip()
    path = str(input("Enter Path or 1-Current, 2-Sports, 3-Temp \n")).lower().strip()

    if len(path) == 0 :
        path = "/Users/henryvalevich/Downloads/Temp Current/"
    elif path == "1":
        path = "/Users/henryvalevich/Downloads/Temp Current/"
    elif path == "2":
        path = "/Users/henryvalevich/Downloads/Temp Sports/"
    elif path == "3":
        path = "/Users/henryvalevich/Downloads/Temp/"

    if os.path.exists(path):
        print('Path: ' + path) 
    else:
        print('Path Does Not Exist!')
        sys.exit()


    concatFiles1_function(path)

#    concatFiles2_function(path)


