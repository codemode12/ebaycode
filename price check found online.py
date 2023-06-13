import xlwings as xw
from bs4 import BeautifulSoup
import requests
import statistics

@xw.func
def get_prices(url,args =[]):
    url = requests.get(url).content
    soup = BeautifulSoup(url,'html.parser')

    products = []
    rsecSel = 'li:not(.srp-river-answer--REWRITE_START ~ li)'
    iDetSel = f'div[id="srp-river-results"] {rsecSel} div.s-item__details'
    results = soup.select(f'{iDetSel}:not(:has(span.s-item__location))')
    for item in results:
        price = item.find('span', class_='s-item__price').text.replace('$', '').replace(',', '')

        if 'to' not in price:
            price = float(price)
            products.append(price)
    
        mean = round(statistics.mean(products), 2)
        median = round(statistics.median(products), 2)

    print (mean, median)

get_prices('https://www.ebay.com/sch/i.html?_nkw=Pokemon+Snorlax+Black+Star+League+Promo+%2349+PSA+9+Mint')