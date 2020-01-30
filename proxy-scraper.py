#!/usr/bin/python3

import requests
from tqdm import tqdm
import threading
import time
import sys
import re


proxies = []

def config():
    try:
        with open(os.path.join(path, 'config.json'), 'r', encoding='utf-8') as setting:
            config = json.load(setting)
            proxies = config['proxies']
            debug = config['debug']
            output = config['output']
            timeout = config['timeout']
            return config
    except:
        print('Failed loading "config.json"')

def fetchAndParseProxies(url, custom_regex):
    n = 0
    try:
        proxylist = requests.get(url, timeout=15).text
        proxylist = proxylist.replace('null', '"N/A"')
        custom_regex = custom_regex.replace('%ip%', '([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3})')
        custom_regex = custom_regex.replace('%port%', '([0-9]{1,5})')
        for proxy in re.findall(re.compile(custom_regex), proxylist):
            proxies.append(proxy[0] + ":" + proxy[1])
            n += 1
    except:
        sys.stdout.write("{0: >5} proxies fetched from {1}\n".format('0',url))

config = config()

proxysources = [
	["http://spys.me/proxy.txt","%ip%:%port% "],
	["http://www.httptunnel.ge/ProxyListForFree.aspx"," target=\"_new\">%ip%:%port%</a>"],
	["https://www.us-proxy.org/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
	["https://free-proxy-list.net/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
	["https://www.sslproxies.org/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
	["https://www.proxy-list.download/api/v0/get?l=en&t=https", '"IP": "%ip%", "PORT": "%port%",'],
	["https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=5000&country=all&anonymity=elite&ssl=all", "%ip%:%port%"],
]


loop = tqdm(total=len(proxysources), position=0, leave=False)
for source in proxysources:
    loop.set_description('fetching...')
    fetchAndParseProxies(source[0], source[1])
    loop.update(1)
loop.close()

def save(i):
    file = open(config['proxies'], "a")
    file.write(i+"\n")
    file.close()

def checker(i):
    try:
        global running
        global good
        global bad
        running += 1
    except:
        running = 0
        bad = 0
        good = 0
    s = requests.session()
    s.proxies = {
        'http':'http://'+i,
        'https':'https://'+i
    }
    try:
        rr = s.get(url, timeout=config['timeout'])
        print('Valid => ',i)
        save(i)
        good += 1
    except requests.exceptions.ReadTimeout:
        print('ReadTimeout => ',i)
        bad += 1
    except requests.exceptions.ConnectTimeout:
        print('ConnectTimeout => ',i)
        bad += 1
    except requests.exceptions.ProxyError:
        print('ProxyError => ',i)
        bad += 1
    except requests.exceptions.SSLError:
        print('SSLError => ',i)
        bad += 1
    except requests.exceptions.ConnectionError:
        print('ConnectionError => ',i)
        bad += 1
    running -= 1

print(len(proxies)," Proxies Fetched.")
url = "https://httpbin.org/ip"
good = 0
bad = 0
running = 0
ch = 0
max = 25
for i in proxies:
    if running < max:
        x = threading.Thread(target=checker, args=(i,))
        x.start()
        ch += 1
    else:
        time.sleep(.1)

time.sleep(3)

print("good : ", good)
print("bad  : ", bad)