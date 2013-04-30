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

        if self.d == 0: # handle the case the day is 0 (day wasn't indicated on wikipedia page)
            self.d = 1
        date = datetime.date(int(self.y), int(self.m), int(self.d))
        
        difference = datetime.timedelta(days=daysPadding)
        beginInterval = date - difference
        endInterval = date + difference

        beginInterval = str(beginInterval.month) + '-' + str(beginInterval.day) + '-' + str(beginInterval.year)
        endInterval = str(endInterval.month) + '-' + str(endInterval.day) + '-' + str(endInterval.year)
        
        return (Date(beginInterval), Date(endInterval))

    #returns an integer representation of the date that makes the date easy to sort
    def numericDate(self):
        year = str(self.y)
        month = str(self.m)
        day = str(self.d)

        if len(year) == 1: year = '0'+ year
        if len(month) == 1: month = '0'+ month
        if len(day) == 1: day = '0'+ day

        return int(year + month + day)

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
        year = ''
        date = ''
        productName = ''
        family = ''
        deathDate = ''
        rowspan = 0
        rowspanFix = 1
        spanSub = 0
        for tr in trs:
            tr = BeautifulSoup(str(tr))
            if len(tr.find_all('td')) != 0:
                tds = tr.find_all('td')
                count = 0
                # if len(tds.find_all('b')) != 0:
                if first == 1:
                  for td in tds:
                    if count == 0:
                      m = re.search('<b>[0-9]+</b>', str(td))
                      year = m.group(0)
                      year = year[3:-4]
                    elif count == 1:
                      #print "Date 1"
                      # m = re.search('>[a-zA-Z0-9\ ]+<', str(td))
                      # date = m.group(0)
                      date = td.text
                      date = date + ' ' + year
                      #print date
                    elif count == 2:
                      #print "Product Name"
                      productName = td.text
                      #print productName
                    elif count == 3:
                      #print "Family"
                      family = td.text
                      #print family
                    elif count == 4:
                      #print "Discontinued Date"
                      deathDate = td.text
                      #print deathDate
                    count += 1
                  first = 0
                  months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                  dateSplit = str(date).split(' ')
                  if ',' in dateSplit[1]: dateSplit[1] = dateSplit[1][:-1]
                  if len(dateSplit) == 3:
                    newD = str(months.index(dateSplit[0])+1)+'-'+dateSplit[1]+'-'+dateSplit[2]
                  else:
                    newD = str(months.index(dateSplit[0])+1)+'-'+'00'+'-'+dateSplit[1]
                  products[productName] = [Date(newD), family, deathDate]
                else:
                  if len(tds) == 3:
                    for td in tds:
                      if count == 0:
                        productName = td.text
                        #print "Product Name"
                        #print productName
                      if count == 1:
                        family = td.text
                        #print "Family"
                        #print family
                      if count == 2:
                        deathDate = td.text
                        #print "Death Date"
                        #print deathDate
                      count += 1
                    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                    dateSplit = str(date).split(' ')
                    if ',' in dateSplit[1]: dateSplit[1] = dateSplit[1][:-1]
                    if len(dateSplit) == 3:
                      newD = str(months.index(dateSplit[0])+1)+'-'+dateSplit[1]+'-'+dateSplit[2]
                    else:
                      newD = str(months.index(dateSplit[0])+1)+'-'+'00'+'-'+dateSplit[1]
                    products[str(productName)] = [Date(newD), str(family), str(deathDate)]
                  elif len(tds) == 4:
                    for td in tds:
                      if count == 0:
                        date = td.text
                        date = date + ' ' + year
                        #print "Date"
                        #print date
                      if count == 1:
                        productName = td.text
                        #print "Product Name"
                        #print productName
                      if count == 2:
                        family = td.text
                        #print "Family"
                        #print family
                      if count == 3:
                        deathDate = td.text
                        #print "Death Date"
                        #print deathDate
                      count += 1
                    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                    dateSplit = str(date).split(' ')
                    if ',' in dateSplit[1]: dateSplit[1] = dateSplit[1][:-1]
                    if len(dateSplit) == 3:
                      newD = str(months.index(dateSplit[0])+1)+'-'+dateSplit[1]+'-'+dateSplit[2]
                    else:
                      newD = str(months.index(dateSplit[0])+1)+'-'+'00'+'-'+dateSplit[1]
                    products[str(productName)] = [Date(newD), str(family), str(deathDate)]
                  #else:
                    #print 'WHAT IS THIS CASE???'
                  #print
            elif len(tr.find_all('th')) != 0:
                ths = tr.find_all('th')
                #print 'ths:'
                #print ths
    # print products
    return products

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
        # print 'Legend:             ' + ulines[0]
        # print 'Starting Date Data: ' + start
        # print 'Ending Date Data:   ' + end
        difference = parse_yahoo_stock(end)['Close'] - parse_yahoo_stock(start)['Close']
        if difference > 0:
            sign = '+'
        else:
            sign = ''
        # print sign + str(difference)

    def addStockData(self, dataFrame, daysPadding=7): # adds stockdata to input dataframe

        for row in dataFrame:
            productDate = row['Release Date']
            dateRange = productDate.dateRange(daysPadding)
            startDate = dateRange[0]
            endDate = dateRange[-1]
            interval = 'd'
            url = "http://ichart.yahoo.com/table.csv?s=%s&a=%i&b=%i&c=%i&d=%i&e=%i&f=%i&g=%s&ignore=.csv" \
                % ( self.symbol, startDate.m-1, startDate.d, startDate.y, endDate.m-1, endDate.d, endDate.y, interval)
            from time import sleep
            
            u = urllib.urlopen(url)
            
            ulines = u.read().split("\n")
            start = ulines[-2]
            end = ulines[1]
            # print 'Legend:             ' + ulines[0]
            # print 'Starting Date Data: ' + start
            # print 'Ending Date Data:   ' + end
            difference = parse_yahoo_stock(end)['Close'] - parse_yahoo_stock(start)['Close']
            if difference > 0:
                sign = '+'
            else:
                sign = ''
            # print sign + str(difference)   
            row['Stock Impact'] = difference 

class Query:
    def __init__(self, queryType, arg, daysPadding=1):
        self.daysPadding = daysPadding
        self.symbol = "AAPL"
        self.queryType = queryType
        self.arg = arg

        # set up the dataFrame
        #queryTypes: "timerange, family, product"
        if queryType=="timerange":
            self.startDate = arg[0].dateRange(daysPadding)[0]
            self.endDate = arg[1].dateRange(daysPadding)[1]
            criterion = timelineDataFrame['Release Date'].map(lambda date: (date.numericDate() > self.startDate.numericDate()) and (date.numericDate() < self.endDate.numericDate()))
            self.dataFrame = timelineDataFrame[criterion]
        elif queryType=="family":
            criterion = timelineDataFrame['Family'] == arg
            self.dataFrame = timelineDataFrame[criterion]
            for date in self.dataFrame['Release Date']:
                dateRange = date.dateRange(daysPadding)
            self.startDate = self.dataFrame['Release Date'][0].dateRange(daysPadding)[0]
            self.endDate = self.dataFrame['Release Date'][-1].dateRange(daysPadding)[1]
        elif queryType=="product":
            self.dataFrame = timelineDataFrame[timelineDataFrame.index == arg]
            dateRange = self.dataFrame['Release Date'].dateRange(daysPadding)
            self.startDate = dateRange[0]
            self.endDate = dateRange[1]
        else:
            print "invalid queryType"

    def plot(self):
        import matplotlib
        self.dataFrame.plot(use_index=True, y='Stock Impact')

    def getIndividualStock

    def getRangeStockData(self):
        interval = 'd'
        url = "http://ichart.yahoo.com/table.csv?s=%s&a=%i&b=%i&c=%i&d=%i&e=%i&f=%i&g=%s&ignore=.csv" \
            % ( self.symbol, self.startDate.m-1, self.startDate.d, self.startDate.y, self.endDate.m-1, self.endDate.d, self.endDate.y, interval)
        from time import sleep
            
        u = urllib.urlopen(url)
            
        ulines = u.read().split("\n")
        start = ulines[-2]
        end = ulines[1]
        
        difference = parse_yahoo_stock(end)['Close'] - parse_yahoo_stock(start)['Close']
        if difference > 0:
            sign = '+'
        else:
            sign = ''
        #print sign + str(difference)   
        return difference

    def setStockData(self):


apple = Company("Apple")
apple.getData() # defaults to time padding of 7 days
# apple.getData(6)
# apple.getData(5)
# apple.getData(4)
# apple.getData(3)
# apple.getData(2)

datahash = getProductReleasesForApple()
# print datahash

import pandas
import matplotlib as plt

timeline = datahash

sortedTimeline = sorted(timeline.items(),key=lambda tup: tup[1][0].numericDate())

productName = []
family = []
releaseDate = []
discontinueDate = []

for item in sortedTimeline:
    productName.append(item[0])
    releaseDate.append(item[1][0])
    family.append(item[1][1])
    discontinueDate.append(item[1][2])

timelineDataFrame = pandas.DataFrame({'Product Name': productName, 'Release Date':releaseDate, 'Family': family,  'Date Discontinued': discontinueDate, 'Stock Impact': 0}).set_index('Product Name')

sampleQuery = Query("family", "Modems")
print sampleQuery.startDate.date
print sampleQuery.endDate.date
print sampleQuery.getStockData()
print sampleQuery.dataFrame
