from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re


req = Request("https://www.ebay.com/sch/i.html?_from=R40&_nkw=pokemon+graded&_sacat=0&LH_Auction=1&_sop=1&_pgn=1")
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "html.parser")

links = soup.find_all('a', class_='s-item__link',)


print(links)