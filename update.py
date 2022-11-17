import os
import re
import time
import requests
from bs4 import BeautifulSoup as bs
from pathlib import Path

print("Removing old user agents...")
#empty the contents of user_agents array in config.json if not empty
def rmold():
    start = time.time()
    with open("config.json", "r") as config:
        conf_old = config.read()
        if conf_old.find("user_agents") != -1:
            os.system("chmod +x update-helper.sh && ./update-helper.sh -c") 
            print ("Old user agents removed.")
            config.close()
        else:
            print("You seem to be running this script for the first time.\n")
            config.close()
    end = time.time()
    print("rmoold() took " + str(end - start) + " seconds to run.")
rmold()

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
chrome = requests.get("https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome", headers=headers)
ff = requests.get("https://www.whatismybrowser.com/guides/the-latest-user-agent/firefox", headers=headers)
safari = requests.get("https://www.whatismybrowser.com/guides/the-latest-user-agent/safari", headers=headers)
edge = requests.get("https://www.whatismybrowser.com/guides/the-latest-user-agent/edge", headers=headers)
opera = requests.get("https://www.whatismybrowser.com/guides/the-latest-user-agent/opera", headers=headers)

soup1 = bs(chrome.text, "lxml")
soup2 = bs(ff.text, "lxml")
soup3 = bs(safari.text, "lxml")
soup4 = bs(edge.text, "lxml")
soup5 = bs(opera.text, "lxml")

print("Obtaining new user agents...")

def scrape_uas():
    start = time.time()
    chrome_uas = soup1.find_all("span", {"class": "code"})
    ff_uas = soup2.find_all("span", {"class": "code"})
    safari_uas = soup3.find_all("span", {"class": "code"})
    edge_uas = soup4.find_all("span", {"class": "code"})
    opera_uas = soup5.find_all("span", {"class": "code"})
    end = time.time()
    print("scrape_uas() took " + str(end - start) + " seconds to run.")
    return chrome_uas, ff_uas, safari_uas, edge_uas, opera_uas

def process_ua(user_agents):
    start = time.time()
    uas = []
    for ua in user_agents:
        if getattr(ua, "text") is not None:
            uas.append(ua.text.split(","))
    end = time.time()
    print("process_ua() took " + str(end - start) + " seconds to run.")
    return uas

user_agents = scrape_uas()

def exportandclean():
    start = time.time()
    tmp = Path("temp.txt")
    tmp.touch(exist_ok=True)
    with open("temp.txt", "r+") as temp:
        chrome_uas, ff_uas, safari_uas, edge_uas, opera_uas = scrape_uas()
        chrome_uas = process_ua(chrome_uas)
        ff_uas = process_ua(ff_uas)
        safari_uas = process_ua(safari_uas)
        edge_uas = process_ua(edge_uas)
        opera_uas = process_ua(opera_uas)
        for chrome_ua in chrome_uas:
            for ua in chrome_ua:
                temp.write(ua + "\n")
        for ff_ua in ff_uas:
                for ua in ff_ua:
                    temp.write(ua + "\n")
        for safari_ua in safari_uas:
            for ua in safari_ua:
                temp.write(ua + "\n")
        for edge_ua in edge_uas:
            for ua in edge_ua:
                temp.write(ua + "\n")
        for opera_ua in opera_uas:
            for ua in opera_ua:
                temp.write(ua + "\n")
        temp.close()
        #append quotation marks to lines beginning with "Mozilla" and ones that end with a number. Use sed
        os.system("chmod +x update-helper.sh")
        os.system("./update-helper.sh -q")
        end = time.time()
        print("exportandclean() took " + str(end - start) + " seconds to run.")
exportandclean()

print("Cleaning things up...")
start = time.time()
os.system("sed -i 's/<span class=\"code\">//g' temp.txt")
os.system("sed -i 's/<\/span>//g' temp.txt")
end = time.time()
print("Cleaning took " + str(end - start) + " seconds to run.")

#if a line ends with "KHTML" and then another starts with "like Gecko", merge them into one line, using re
with open("temp.txt", "r+") as temp:
    start = time.time()
    lines = temp.readlines()
    temp.seek(0)
    temp.truncate()
    for line in lines:
        if line.endswith("KHTML") and lines[lines.index(line) + 1].startswith("like Gecko"):
            #merge the line with the next line
            line = line.rstrip("KHTML") + lines[lines.index(line) + 1]
    temp.writelines(lines)
    temp.close()
    end = time.time()
    print("Merging lines took " + str(end - start) + " seconds to run.")

start = time.time()
# create a ua_list variable from the contents of temp.txt
with open("temp.txt", "r") as temp:
    ua_list = temp.read()
    temp.close()
# paste the contents of ua_list to user_agents array in config.json and remove temp.txt. We also need to remove the last comma from the last line of config.json.
with open("config.json", "r") as config:
    config = config.read()
    if config.find("user_agents") != -1:
        conf = config.replace("user_agents: []", "user_agents: " + ua_list)
        conf = str(config.replace(",]", "]"))
        with open("config.json", "w") as cfg:
            cfg.write(conf)
            cfg.close()
end = time.time()
print("Updating config.json took " + str(end - start) + " seconds to run.")
#os.system("rm temp.txt")
print("Done!")

