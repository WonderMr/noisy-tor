import requests
import lxml
import os
from bs4 import BeautifulSoup as bs

print ("Removing old user agents...")
#empty the contents of user_agents array in config.json if not empty
def rmold():
    with open("config.json", "r") as config:
        conf_old = config.read()
        if conf_old.find("user_agents") != -1:
            os.system("chmod +x update-helper.sh && ./update-helper.sh -c") 
            print ("Old user agents removed.")
            config.close()
        else:
            print("You seem to be running this script for the first time.\n")
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
    chrome_uas = soup1.find_all("span", {"class": "code"})
    ff_uas = soup2.find_all("span", {"class": "code"})
    safari_uas = soup3.find_all("span", {"class": "code"})
    edge_uas = soup4.find_all("span", {"class": "code"})
    opera_uas = soup5.find_all("span", {"class": "code"})
    return chrome_uas, ff_uas, safari_uas, edge_uas, opera_uas

def process_ua(user_agents):
    uas = []
    for ua in user_agents:
        if getattr(ua, "text") is not None:
            uas.append(ua.text.split(","))
    return uas

user_agents = scrape_uas()

def exportandclean():
    with open("temp.txt", "r+") as temp:
        chrome_uas, ff_uas, safari_uas, edge_uas, opera_uas = scrape_uas()
        chrome_uas = process_ua(chrome_uas)
        ff_uas = process_ua(ff_uas)
        safari_uas = process_ua(safari_uas)
        edge_uas = process_ua(edge_uas)
        opera_uas = process_ua(opera_uas)
        for chrome_ua in chrome_uas:
            for chrome_ua_ in chrome_ua:
                temp.write(chrome_ua_ + "\n")
        for ff_ua in ff_uas:
            for ff_ua_ in ff_ua:
                temp.write(ff_ua_ + "\n")
        for safari_ua in safari_uas:
            for safari_ua_ in safari_ua:
                temp.write(safari_ua_ + "\n")
        for edge_ua in edge_uas:
            for edge_ua_ in edge_ua:
                temp.write(edge_ua_ + "\n")
        for opera_ua in opera_uas:
            for opera_ua_ in opera_ua:
                temp.write(opera_ua_ + "\n")
        temp.close()
        #append quotation marks to lines beginning with "Mozilla" and ones that end with a number. Use sed
        os.system("chmod +x update-helper.sh && ./update-helper.sh -q")


exportandclean()

print("Cleaning things up...")

os.system("sed -i 's/<span class=\"code\">//g' temp.txt")
os.system("sed -i 's/<\/span>//g' temp.txt")

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
#os.system("rm temp.txt")
print("Done!")

