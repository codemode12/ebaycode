import requests
from bs4 import BeautifulSoup

payload = {'_nkw': 'cards'}
r = requests.post('https://www.ebay.com/sch/i.html', data=payload)
print(r.status_code)