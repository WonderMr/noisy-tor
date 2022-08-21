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

soup1 = bs(chrome.text, "lxml")
soup2 = bs(ff.text, "lxml")
soup3 = bs(safari.text, "lxml")
soup4 = bs(edge.text, "lxml")
soup5 = bs(opera.text, "lxml")

soups = [soup1, soup2, soup3, soup4, soup5]

def uasw():
    for s in soups:
        for ua in s.select(".code"):
            with open('config.json', 'r+') as c:
                for line in c:
                    if line.contains('user_agents'):
                        lines[i] = lines[i].strip() + c.write("\"{ua}\",\n\"{ua}\"")
                c.seek(0)
                for line in lines:
                    c.write(line)
    
uasw.chrome()
uasw.ff()
uasw.safari()
uasw.edge()
uasw.opera()
