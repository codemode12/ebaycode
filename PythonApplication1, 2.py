import requests
from bs4 import BeautifulSoup

#page number counter- allows me to change URL accordingly
countNum = 1
#2 URLs- 1 for buy now and 1 for auctions
#baseURL = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=pokemon+graded&_sacat=0&LH_TitleDesc=0&_fsrp=1&LH_BIN=1&_sop=10&_pgn='
baseURL = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=pokemon+graded&_sacat=0&LH_Auction=1&_sop=1&_pgn='

#can change this to page number you want to go until
while countNum < 5:
    #URL to be used in code which adds in the page number calculated above
    url = baseURL + str(countNum)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    #finds all prices
    prices = soup.find_all('span', class_='s-item__price')
    #finds all names 
    names = soup.find_all('div', class_='s-item__title')
    #This loop does this whole thing to every listing name it finds for the amount of names found 
    for i in range (0, len(names)):
        #this makes the name able to be placed into the URL by replacing whitespace with +
        preName1 = (names[i].text).replace(' ', '+')
        #was encountering a problem where first search result was always 'Shop on eBay' and would causes errors later so this just removes that result
        preName2 = preName1.replace('Shop+on+eBay', '')
        searchName = str(preName2)
        if '@ccount' not in searchName:
            #new URL to look up sold prices of listing. Takes generic URL of every sold listing and inserts searchName of specific listing being looked at and converts it to a string
            search = ('https://www.ebay.com/sch/i.html?_from=R40&_nkw=' + searchName + '&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1')
            soldURL = str(search)
            soldResponse = requests.get(soldURL)
            finalSoup = BeautifulSoup(soldResponse.text, 'html.parser')
            #finds all prices on page of sold listings
            soldPrices = finalSoup.find_all('span', class_='s-item__price')
            #finds all names on page of sold listings (Not sure if this is needed but used for sake of continuity since other for loop was for len(names) not len(prices))
            soldNames = finalSoup.find_all('div', class_='s-item__title')
            #creates empty list to be filled with each sold price found
            priceList = []
            soldNameLen = len(soldNames)
            soldPriceLen = len(soldPrices)
            #very similar to for loop this is embedded in. iterates through each sold price
            for j in range (0, soldNameLen):
                #Checks if length of the price is too long (because was encountering error where price would be '1.99 to 34.99', for example, 
                #so I check if the price in its correct format is too long, which most likely means it looks like this). Can prob remove else
                if len(soldPrices[j].text.replace('$', '').replace(',', '')) < 7:
                    #removes unwanted characters in price and turns prices into integers since were Tags before
                    priceList.append((soldPrices[j].text).replace('$', '').replace(',', ''))
            priceList = [int(float(i)) for i in priceList]
                    #reformats original price we need to compare average to, and changes to float
            almostOrigPrice = prices[i].text.replace('$', '').replace(',', '')
            origPrice = (float(almostOrigPrice))
            #checks if there are no search results
            if soldPriceLen == 0:
                print('No Sold Prices')
            else:
                #takes average
                avgSoldPrice = sum(priceList) / soldPriceLen
                #if meets criteria, prints an alert to check it
                if origPrice/avgSoldPrice < 0.5 and avgSoldPrice > 30:
                    print(names[i].text + '  Worth Checking At: ' + str(origPrice) + ' VS ' + str(avgSoldPrice) + ' on page ' + str(countNum))       
    countNum += 1
