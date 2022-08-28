import requests
import lxml
from bs4 import BeautifulSoup as bs
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
chrome = requests.get("https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome", headers=headers)
ff = requests.get("https://www.whatismybrowser.com/guides/the-latest-user-agent/firefox", headers=headers)
safari = requests.get("https://www.whatismybrowser.com/guides/the-latest-user-agent/safari", headers=headers)
edge = requests.get("https://www.whatismybrowser.com/guides/the-latest-user-agent/edge", headers=headers)
opera = requests.get("https://www.whatismybrowser.com/guides/the-latest-user-agent/opera", headers=headers)

#create a beautiful soup object for each of the variables above. The user agent is contained in the .code class
soup1 = bs(chrome.text, "lxml")
soup2 = bs(ff.text, "lxml")
soup3 = bs(safari.text, "lxml")
soup4 = bs(edge.text, "lxml")
soup5 = bs(opera.text, "lxml")



#create a user agent scraper for chrome, firefox, safari, edge, opera using beautiful soup
#user agent is  a single line of text contained in the .code class
#use the getattr function to get the user agent for each browser
#each class contains a string with the user agent, e.g. Mozilla
def scrape_ua(soup):
    for line in soup.find_all("div", class_="code"):
        return line.text

#write the user agent to config.json, to the user_agents array


#write the user agent to config.json, to the user_agents array
def write_ua():
    with open("config.json", "r") as config:
        data = config.read()
        data = data.replace("chrome_ua", chrome_ua())
        data = data.replace("ff_ua", ff_ua())
        data = data.replace("safari_ua", safari_ua())
        data = data.replace("edge_ua", edge_ua())
        data = data.replace("opera_ua", opera_ua())
        with open("config.json", "w") as config:
            config.write(data)

write_ua()
