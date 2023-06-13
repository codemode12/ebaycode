import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

#page number counter- allows me to change URL accordingly
countNum = 1
#2 URLs- 1 for buy now and 1 for auctions
#baseURL = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=pokemon+graded&_sacat=0&LH_TitleDesc=0&_fsrp=1&LH_BIN=1&_sop=10&_pgn='
baseURL = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=pokemon+graded&_sacat=0&LH_Auction=1&_sop=1&_pgn='

#can change this to page number you want to go until
while countNum < 10:
#GETTING INFO OF WHOLE PAGE
    url = baseURL + str(countNum)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', class_='s-item__link')
    prices = soup.find_all('span', class_='s-item__price')
    names = soup.find_all('div', class_='s-item__title')
#LIST COMPRISED OF LINK FOR EACH LISTING
    linkList = []
    for origLink in links:
        linkList.append(origLink.get('href'))
#LIST COMPRISED OF PRICE FOR EACH LISTING
    priceList = []
    for origPrice in prices:
        priceList.append(origPrice.text.replace('$','').replace(',',''))
#LIST COMPRISED OF NAME FOR EACH LISTING
    nameList = []
    for origName in names:
        nameList.append(origName.text)
#FROM HERE START TO WORK ON SINGLE URL
    for embedURL in range(1, len(priceList)):
#GET ALL SOUP INFO FOR SOLD_URL, WHICH IS URL OF LISTING WE ARE LOOKING AT
        sold_url = linkList[embedURL]
        sold_response = requests.get(sold_url)
        sold_soup = BeautifulSoup(sold_response.text, 'html.parser')
#THESE ARE THE SECTIONS THAT ARE COMPRISED OF THE SECTION NAME (WHICH WE USE AS AN IDENTIFIER) AND INFO IT STORES (WHICH WE MAY WANT)
        sold_search_section = sold_soup.find_all('div', class_='ux-layout-section-evo__col')
#LIST I WILL NEED TO FILTER OUT USEFUL INFO FROM USING THE IDENTIFIERS
        name_attributes = []
#LIST THAT WILL STORE THE FINAL INFO I NEED
        search_terms = []
#ALL FILTERS FOR THE NAME_ATTRIBUTES. AT THE END WILL APPEND TO SEARCH_TERMS 
        for attribute in sold_search_section:
            unfiltered_attributes = attribute.find_all('span', class_='ux-textspans')
            for unfilteredAttribute in unfiltered_attributes:
                if 'Condition' not in str(unfiltered_attributes):
                    name_attributes.append(unfilteredAttribute)
        for index, nameAttribute in enumerate(name_attributes):
            if(index<(len(name_attributes)-1)):
                next_nameAttribute = name_attributes[index+1].text
#THESE ARE THE FINAL FILTERS. IF MEETS ANY OF THE CATEGORIES WILL BE ADDED TO SEARCH_TERMS
                if 'Character' in str(nameAttribute) or 'Card Name' in str(nameAttribute):
                    if next_nameAttribute not in search_terms:
                        search_terms.append(next_nameAttribute)
                if 'Set' in str(nameAttribute):
                    if next_nameAttribute not in search_terms:
                        search_terms.append(next_nameAttribute)
                if 'Year Manufactured' in str(nameAttribute) and 'Country' not in str(nameAttribute):
                    if next_nameAttribute not in search_terms:
                        search_terms.append(next_nameAttribute)
                if 'Card Number' in str(nameAttribute):
                    if next_nameAttribute not in search_terms:
                        search_terms.append(next_nameAttribute)
                if 'Grade' in str(nameAttribute) and 'Graded' not in str(nameAttribute) and 'Grader' not in str(nameAttribute):
                    if next_nameAttribute not in search_terms:
                        search_terms.append('Graded ' + next_nameAttribute)
        if len(search_terms) < 5:
                final_search_terms = nameList[embedURL].replace(' ', '+')
                #EMBEDDING INTO THE URL
                search = ('https://www.ebay.com/sch/i.html?_from=R40&_nkw=' + final_search_terms + '&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1')
        else:
                #TURNS MY LIST OF SEARCH_TERMS INTO STRINGS
                string_search_terms = ' '.join(search_terms)
                #ADDS '+' TO THE ITEMS IN THE LIST SO THEY CAN BE INSERTED INTO THE URL
                final_search_terms = string_search_terms.replace(' ', '+')
                #EMBEDDING INTO THE URL
                search = ('https://www.ebay.com/sch/i.html?_from=R40&_nkw=' + final_search_terms + '&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1')
#TURNING URL INTO A STRING AND THEN SOUPING ITS INFORMATION (THIS IS THE SEARCHING UP OF THE SOLD/COMPS IN ORDER TO COMPARE PRICES)
        sold_prices_URL = str(search)
        soldResponse = requests.get(sold_prices_URL)
        sold_soup = BeautifulSoup(soldResponse.text, 'html.parser')
        rsecSel = 'li:not(.srp-river-answer--REWRITE_START ~ li)'
        iDetSel = f'div[id="srp-river-results"] {rsecSel} div.s-item__details'
        finalSoup = sold_soup.select(f'{iDetSel}:not(:has(span.s-item__location))')
        sold_price_list = []
#THIS LOOP GOES THROUGH EACH SOLD ITEM FOUND AND GETS INFO
        for sold_item in finalSoup:
            sold_item_price = sold_item.find('span', class_='s-item__price').text.replace('$', '').replace(',', '')
            if 'to' not in sold_item_price:
                sold_item_price = float(sold_item_price)
                sold_price_list.append(sold_item_price)
        #turns sold price list into integers so their average can be found
        sold_price_list = [int(unfiltered_price) for unfiltered_price in sold_price_list]
#PRICE OF ITEM WE ARE CHECKING (THE EMBED URL ITEM) IS REFORMATTED SO IT CAN BE CALCULATED
        almostOrigPrice = priceList[embedURL]
        origPrice = (float(almostOrigPrice))
    #checks if there are no search results
        if len(sold_price_list) == 0:
                print('No Sold Prices')
        else:
                    #takes average
            formatted_sold_price_list = [int(float(x)) for x in sold_price_list]
            avgSoldPrice = sum(formatted_sold_price_list) / len(formatted_sold_price_list)
                    #if meets criteria, prints an alert to check it
            if origPrice/avgSoldPrice < 0.5 and avgSoldPrice > 30:
                print(nameList[embedURL] + '  Worth Checking At: ' + str(origPrice) + ' VS ' + str(avgSoldPrice) + ' on page ' + str(countNum))
    countNum += 1
print('done')