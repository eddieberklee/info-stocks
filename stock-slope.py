import urllib
import re

class Date:
    def __init__(self, date):
        splitDate = date.split('-')

        self.date = date
        self.m = int(splitDate[0])
        self.d = int(splitDate[1])
        self.y = int(splitDate[2])

    # returns (start date, end date)
    def dateRange(self, daysPadding): # daysPadding is in days
        import datetime
        date = datetime.date(int(self.y), int(self.m), int(self.d))
        
        difference = datetime.timedelta(days=daysPadding)
        beginInterval = date - difference
        endInterval = date + difference

        beginInterval = str(beginInterval.month) + '-' + str(beginInterval.day) + '-' + str(beginInterval.year)
        endInterval = str(endInterval.month) + '-' + str(endInterval.day) + '-' + str(endInterval.year)
        print beginInterval
        print endInterval

        return (Date(beginInterval), Date(endInterval))

def parse_yahoo_stock(line):
    parts = line.split(',')
    parts_dict = {}
    # for product releases there may be a difference between diff('high', 'close')
    # as opposed to more steady differences for a 'normal' non-release day
    legends = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
    floats = [0, 1, 1, 1, 1, 0, 1]
    for i in range(len(parts)):
        if i == 5:
            parts_dict[legends[i]] = int(parts[i])
        if floats[i]:
            parts_dict[legends[i]] = float(parts[i])
        else:
            parts_dict[legends[i]] = parts[i]
    return parts_dict

def getProductReleasesForApple():
    import urllib, urllib2
    from bs4 import BeautifulSoup
    import re
    article = "Timeline of Apple Inc. products"
    article = urllib.quote(article) # sanitize

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')] # wikipedia blocks obvious bot attempts
    
    resource = opener.open("http://en.wikipedia.org/wiki/"+article)
    data = resource.read()
    resource.close()
    
    soup = BeautifulSoup(data)

    # print soup.find('div',id="bodyContent")


    bodyContent = soup.find('div',id="bodyContent")
    wikitables = bodyContent.find_all('table',class_="wikitable")

    products = {}

    for wikitable in wikitables:
        m = re.search('<b>[0-9]+</b>', str(wikitable))
        year = m.group(0)
        # if first == 0:
        # first = 1
        first = 1
        trs = wikitable.find_all('tr')
        for tr in trs:
            tr = BeautifulSoup(str(tr))
            if len(tr.find_all('td')) != 0:
                tds = tr.find_all('td')
                count = 0
                # if len(tds.find_all('b')) != 0:
                year = ''
                date = ''
                productName = ''
                family = ''
                deathDate = ''
                if first == 1:
                  for td in tds:
                    if count == 0:
                      m = re.search('<b>[0-9]+</b>', str(td))
                      year = m.group(0)
                      year = year[3:-4]
                    elif count == 1:
                      print "Date"
                      # m = re.search('>[a-zA-Z0-9\ ]+<', str(td))
                      # date = m.group(0)
                      date = td.text
                      date = date + ' ' + year
                      print date
                    elif count == 2:
                      print "Product Name"
                      productName = td.text
                      print productName
                    elif count == 3:
                      print "Family"
                      family = td.text
                      print family
                    elif count == 4:
                      print "Discontinued Date"
                      deathDate = td.text
                      print deathDate
                    count += 1
                  first = 0
                  products[productName] = [date, family, deathDate]
                else:
                  print year
                  for td in tds:
                    if count == 0:
                      print "Date"
                      date = td.text
                      date = date + ' ' + year
                      print date
                    elif count == 1:
                      print "Product Name"
                      productName = td.text
                      print productName
                    elif count == 2:
                      print "Family"
                      family = td.text
                      print family
                    elif count == 3:
                      print "Discontinued Date"
                      deathDate = td.text
                      print deathDate
                    count += 1
            elif len(tr.find_all('th')) != 0:
                ths = tr.find_all('th')
                print 'ths:'
                print ths

        # trs = "".join(str(tr) for tr in trs)
        # trs = BeautifulSoup(trs)
        # tds = trs.find_all('td')
        # count = 0
        # for td in tds:
        #     print td
        #     print count
        #     count += 1
        #     if count == 0:
        #         print "TITLE TITLE TITLE"
        #     if count % 4 == 0:
        #         print "PRODUCT PRODUCT PRODUCT"

        timeline = {}
        # timeline[productName] = [date, family]

        # columns = [productName, family, stockSlope]
        # Date (Month Day Yearkk)
        # Product Name
        # Family

class Company:
    def __init__(self, name):
        self.name = name
        self.companyToSymbol() # sets self.symbol
        self.releaseDates() # sets self.releaseDates
    def __str__(self):
        return str(self.__dict__.keys())
    def companyToSymbol(self):
        url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=%s&callback=YAHOO.Finance.SymbolSuggest.ssCallback" \
            % self.name
        u = urllib.urlopen(url)
        data = u.read()
        m = re.search('symbol\":\"[a-zA-Z]*\"', data)
        symbol = m.group(0)
        symbol = symbol.split(':')[1][1:-1]
        self.symbol = symbol
        return symbol
    def releaseDates(self):
        self.release_dates = {
            'iBooks Author' : '1-19-2012',
            'iPad (3rd gen)' : '3-16-2012',
            'Apple TV (3rd gen)' : '3-16-2012',
            'Mac Pro (Mid 2012)' : '6-11-2012',
            'Macbook Air (Mid 2012)' : '6-11-2012',
        }
    def getData(self, daysPadding=7):
        productDate = Date(self.release_dates['Apple TV (3rd gen)'])
        dateRange = productDate.dateRange(daysPadding)
        startDate = dateRange[0]
        endDate = dateRange[-1]
        interval = 'd'
        url = "http://ichart.yahoo.com/table.csv?s=%s&a=%i&b=%i&c=%i&d=%i&e=%i&f=%i&g=%s&ignore=.csv" \
            % ( self.symbol, startDate.m-1, startDate.d, startDate.y, endDate.m-1, endDate.d, endDate.y, interval)
        from time import sleep
        # try:
        u = urllib.urlopen(url)
        # except IOError as e:
        #     print "I/O Error ({0}): {1}".format(e.errno, e.strerror)
        #     sleep(3)
        #     return this.getData(daysPadding)

        ulines = u.read().split("\n")
        start = ulines[-2]
        end = ulines[1]
        print 'Legend:             ' + ulines[0]
        print 'Starting Date Data: ' + start
        print 'Ending Date Data:   ' + end
        difference = parse_yahoo_stock(end)['Close'] - parse_yahoo_stock(start)['Close']
        if difference > 0:
            sign = '+'
        else:
            sign = ''
        print sign + str(difference)

apple = Company("Apple")
apple.getData()
apple.getData(6)
apple.getData(5)
apple.getData(4)
apple.getData(3)
apple.getData(2)

getProductReleasesForApple()


# timeline = {}
# timeline[productName] = [date, family]

# columns = [productName, family, stockSlope]
# Date (Month Day Year)
# Product Name
# Family
# Stock Slope

"""
import pandas
import matplotlib as plt

productName = timeline.keys()
family = []
releaseDate = []
stockSlope = []

for value in timeline.values():
    family.append(value[0])
    releaseDate.append(value[1])
    stockSlope.append(value[2])

timelineDataFrame = pandas.DataFrame({'Product Name': timeline.keys(), 'Family': family, 'Release Date':releaseDate, 'Stock Impact': stockSlope}).set_index('Product Name')

timelineDataFrame.plot(use_index=True, y='Stock Impact')
"""
