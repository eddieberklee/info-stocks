import urllib
import re

class Date:
    def __init__(self, date):
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        if re.search('[a-zA-Z]{3}\ [0-9]{1,2},\ [0-9]{4}',date):
            splitDate = date.split(' ')

            threeLetterMonths = map(lambda month: month[:3], months)

            self.m = int(threeLetterMonths.index(splitDate[0])+1)

            if ',' in splitDate[1]:
                self.d = int(splitDate[1].replace(',',''))
            self.y = int(splitDate[2])
            self.date = `self.m` + '-' + `self.d` + '-' + `self.y`
        else:
            splitDate = date.split('-')
            self.date = date
            self.m = int(splitDate[0])
            self.d = int(splitDate[1])
            self.y = int(splitDate[2])

    def __repr__(self):
        # return str('Date(' + self.date + ')')
        return str(self.date)

    # returns (start date, end date)
    def dateRange(self, daysPadding): # daysPadding is in days
        import datetime

        if self.d == 0: # handle the case the day is 0 (day wasn't indicated on wikipedia page)
            self.d = 1
        date = datetime.date(int(self.y), int(self.m), int(self.d))
        
        difference = datetime.timedelta(days=daysPadding)
        beginInterval = date - difference
        endInterval = date + difference
        earliestDate = datetime.date(1985, 9, 2)

        # earliest borderline check
        if beginInterval < earliestDate:
            # print "this should print"
            
            beginInterval = earliestDate
            endInterval = beginInterval + difference + difference
            beginInterval = str(beginInterval.month) + '-' + str(beginInterval.day) + '-' + str(beginInterval.year)
            endInterval = str(endInterval.month) + '-' + str(endInterval.day) + '-' + str(endInterval.year)
            return (Date(beginInterval), Date(endInterval))

        else:
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

"""
class TenQ:
    def __init__(self):
        # self.links = self.getAllSecFilingsLinks
        pass

    def parseSingle(self, link):
        from bs4 import BeautifulSoup
        import urllib
        import re
        html = urllib.urlopen(link).read()
        soup = BeautifulSoup(html)

        # Condensed Consolidated Statements of Operations (Unaudited)
        tempi = html.lower().find('condensed consolidated statements of operations (unaudited)')
        csoup = BeautifulSoup(html[tempi:])
        csoup = BeautifulSoup(str(csoup.find('table')))
        trs = csoup.findAll('tr')
        for tr in trs:
            tr = BeautifulSoup(str(tr))
            trtext = tr.text.strip()
            # go through each td instead of trying to parse tr stuff
            print trtext
            labels = re.search('[a-zA-Z\ ][a-zA-Z\ ]*',trtext)
            print labels.group(0)
            print trtext.split('  ')
            if len(trtext.split()) > 0:
                pass
            # print tr.findAll('td', {'align':'RIGHT'})

    def getAllSecFilingsLinks(self):
        from bs4 import BeautifulSoup
        import re
        firsturl = 'http://investor.apple.com/sec.cfm?DocType=Quarterly&DocTypeExclude=&SortOrder=FilingDate%20Descending&Year=&Pagenum=1&FormatFilter=&CIK='
        pagesLeft = True
        links = {}

        print 'Scraping all 10-Q HTML Links...'

        while pagesLeft == True:
            html = urllib.urlopen(firsturl).read()
            soup = BeautifulSoup(html)

            try:
                message = BeautifulSoup(str(soup.find('div',id='main'))).find('div',{'class':'table-wrapper'}).find('p').text
            except:
                message = 'Could not find means there are more pages to search'
            if message == 'There are no Quarterly filings available.': pagesLeft = False; break

            filingsTable = BeautifulSoup(str(soup.find('table',id='filings-table')))

            trs = BeautifulSoup(str(filingsTable.find_all('tr')))
            for tr in trs:
                tds = BeautifulSoup(str(tr)).find_all('td')
                if len(tds) >= 1:
                    lastTD = tds[-1]
                    a = BeautifulSoup(str(lastTD)).find('a')
                    a = str(a)
                    m = re.search('href="[a-zA-Z\?\.\=0-9\-\&;]*"', a)
                    link = m.group(0)[6:-1]

                    filing = tds[0]
                    filing = filing.text

                    date = tds[2]
                    date = Date(date.text)

                    if filing == '10-Q':
                        links[date] = 'http://investor.apple.com/' + link

            newlink = 'http://investor.apple.com' + BeautifulSoup(str(soup.find('div',{'class':'table-nav rounded clearme'}))).findAll('a')[-2]['href']

            firsturl = newlink

        # print links

        htmlLinks = {}

        for date in links.keys():
            link = links[date]
            testLink = link
            soup = BeautifulSoup(urllib.urlopen(testLink).read())

            fileDate = soup.find('meta')['content']

            frames = soup.find_all('frame')
            actualFrame = str(frames[1])
            m = re.search('src="[a-zA-Z\?\.\=0-9\-\&;:\/]*"', actualFrame)
            actualLink = m.group(0)[5:-1]

            links[date] = actualLink
        return links
"""

# t = TenQ()
# t.parseSingle('http://apps.shareholder.com/sec/viewerContent.aspx?companyid=AAPL&docid=9236741')

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
                      # m = re.search('>[a-zA-Z0-9\ ]+<', str(td))
                      # date = m.group(0)
                      date = td.text
                      date = date + ' ' + year
                    elif count == 2:
                      productName = td.text
                    elif count == 3:
                      family = td.text
                    elif count == 4:
                      deathDate = td.text
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
                      if count == 1:
                        family = td.text
                      if count == 2:
                        deathDate = td.text
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
                      if count == 1:
                        productName = td.text
                      if count == 2:
                        family = td.text
                      if count == 3:
                        deathDate = td.text
                      count += 1
                    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                    dateSplit = str(date).split(' ')
                    if ',' in dateSplit[1]: dateSplit[1] = dateSplit[1][:-1]
                    if len(dateSplit) == 3:
                      newD = str(months.index(dateSplit[0])+1)+'-'+dateSplit[1]+'-'+dateSplit[2]
                    else:
                      newD = str(months.index(dateSplit[0])+1)+'-'+'00'+'-'+dateSplit[1]
                    products[str(productName)] = [Date(newD), str(family), str(deathDate)]
            elif len(tr.find_all('th')) != 0:
                ths = tr.find_all('th')
    return products 

class Query:
    #queryTypes: "timerange, family, product"
    def __init__(self, queryType, arg, daysPadding=1):
        self.daysPadding = daysPadding
        self.symbol = "AAPL"
        self.queryType = queryType
        self.arg = arg

        # set up the dataFrame
        if queryType=="timerange":
            self.startDate = arg[0].dateRange(daysPadding)[0]
            self.endDate = arg[1].dateRange(daysPadding)[1]
            # self.dateBoundary()
            criterion = timelineDataFrame['Release Date'].map(lambda date: (date.numericDate() > self.startDate.numericDate()) and (date.numericDate() < self.endDate.numericDate()))
            self.dataFrame = timelineDataFrame[criterion]
        elif queryType=="family":
            criterion = timelineDataFrame['Family'] == arg
            self.dataFrame = timelineDataFrame[criterion]
            for date in self.dataFrame['Release Date']:
                dateRange = date.dateRange(daysPadding)
            self.startDate = self.dataFrame['Release Date'][0].dateRange(daysPadding)[0]
            self.endDate = self.dataFrame['Release Date'][-1].dateRange(daysPadding)[1]
            # self.dateBoundary()
        elif queryType=="product":
            self.dataFrame = timelineDataFrame[timelineDataFrame.index == arg]
            dateRange = self.dataFrame['Release Date'][0].dateRange(daysPadding)
            self.startDate = dateRange[0]
            self.endDate = dateRange[1]
            # self.dateBoundary()
        else:
            print "invalid queryType"

        self.setStockData()
        print self.dataFrame

    # def dateBoundary(self):
    #     dateBoundary = Date("9-2-1985")
    #     if self.startDate.numericDate() < dateBoundary.numericDate():
    #         print "startDate goes past the  information we have. startDate set to earliest possible date."
    #         self.startDate = dateBoundary

    def plotIndividualStockDifferences(self):
        import matplotlib.pyplot as plt
        plot = mouseHoverPlot(self.dataFrame['Individual Stock Difference'], self.dataFrame)
        pl.ylabel('Stock Difference over %d day(s) in dollars' % self.daysPadding)
        pl.show()

    def plotSlopeChanges(self):
        import matplotlib.pyplot as plt
        self.dataFrame.plot(use_index=True, y='Stock Slope Change')
        plt.show()

    def getIndividualStock(self, releaseDate):
        dateRange = releaseDate.dateRange(self.daysPadding)
        startIndividualDate = dateRange[0]
        endIndividualDate = dateRange[1]

        interval = 'd'
        url = "http://ichart.yahoo.com/table.csv?s=%s&a=%i&b=%i&c=%i&d=%i&e=%i&f=%i&g=%s&ignore=.csv" \
            % ( self.symbol, startIndividualDate.m-1, startIndividualDate.d, startIndividualDate.y, endIndividualDate.m-1, endIndividualDate.d, endIndividualDate.y, interval)
        from time import sleep
            
        u = urllib.urlopen(url)
            
        ulines = u.read().split("\n")
        start = ulines[-2]
        end = ulines[1]
        
        difference = parse_yahoo_stock(end)['Close'] - parse_yahoo_stock(start)['Close']
        if difference > 0:
            sign = '+'
        else:
            sign = '-'
        #print sign + str(difference)   
        return difference

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
            sign = '-'
        #print sign + str(difference)   
        return difference

    def getStockSlope(self, releaseDate):
        interval = 'd'
        url = "http://ichart.yahoo.com/table.csv?s=%s&a=%i&b=%i&c=%i&d=%i&e=%i&f=%i&g=%s&ignore=.csv" \
            % ( self.symbol, self.startDate.m-1, self.startDate.d, self.startDate.y, releaseDate.m-1, releaseDate.d, releaseDate.y, interval)
        from time import sleep
        u = urllib.urlopen(url)
        ulines = u.read().split("\n")
        start = ulines[-2]
        end = ulines[1]
        leadingDifference = parse_yahoo_stock(end)['Close'] - parse_yahoo_stock(start)['Close']
        leadingSlope = leadingDifference / self.daysPadding

        url = "http://ichart.yahoo.com/table.csv?s=%s&a=%i&b=%i&c=%i&d=%i&e=%i&f=%i&g=%s&ignore=.csv" \
            % ( self.symbol, releaseDate.m-1, releaseDate.d, releaseDate.y, self.endDate.m-1, self.endDate.d, self.endDate.y, interval)
        from time import sleep
        u = urllib.urlopen(url)
        ulines = u.read().split("\n")
        start = ulines[-2]
        end = ulines[1]
        leavingDifference = parse_yahoo_stock(end)['Close'] - parse_yahoo_stock(start)['Close']
        leavingSlope = leavingDifference / self.daysPadding

        slopeDifference = leavingSlope - leadingSlope
        return slopeDifference       

    def setStockData(self): # should set both RangeStock and IndividualStock
        rangeStockImpact = self.getRangeStockData()
        self.dataFrame['Range Stock Difference'] = rangeStockImpact
        indivStocks = []
        stockSlopes = []
        for date in self.dataFrame['Release Date']:
            indivStocks.append(self.getIndividualStock(date))
            stockSlopes.append(self.getStockSlope(date))
        self.dataFrame['Individual Stock Difference'] = indivStocks
        self.dataFrame['Stock Slope Change'] = stockSlopes
        
    #returns row of most influential product
    def getMostInfluencial(self):
        maxIndex = self.dataFrame['Individual Stock Difference'].argmax()
        maxProduct = self.dataFrame.index[maxIndex]
        maxProductRow = self.dataFrame[self.dataFrame.index == maxProduct]
        return maxProductRow

import matplotlib as plt
plt.use('WXAgg')
plt.interactive(False)

import pylab as pl
from pylab import get_current_fig_manager as gcfm
import wx
import numpy as np
import random

class mouseHoverPlot(object):
    def __init__(self, dataY, dataFrame):
        self.dataFrame = dataFrame
        self.figure = pl.figure()
        self.axis = self.figure.add_subplot(111)
        # create a long tooltip with newline to get around wx bug (in v2.6.3.3)
        # where newlines aren't recognized on subsequent self.tooltip.SetTip() calls
        self.tooltip = wx.ToolTip(tip='tip with a long %s line and a newline\n' % (' '*100))
        gcfm().canvas.SetToolTip(self.tooltip)
        self.tooltip.Enable(False)
        self.tooltip.SetDelay(0)
        self.figure.canvas.mpl_connect('motion_notify_event', self._onMotion)
        self.dataX = range(len(dataY))
        self.dataY = dataY
        self.xTicks = dataFrame.index
        pl.xticks(self.dataX, self.xTicks)
        self.axis.plot(self.dataX, self.dataY, linestyle='-', marker='o', markersize=15, label='myplot')

    def _onMotion(self, event):
        collisionFound = False
        if event.xdata != None and event.ydata != None: # mouse is inside the axes
            for i in xrange(len(self.dataX)):
                radius = .2
                if abs(event.xdata - self.dataX[i]) < radius and abs(event.ydata - self.dataY[i]) < radius:
                    def productName(xPos):
                        return self.xTicks[int(round(xPos))]
                    # print self.dataFrame[self.dataFrame.index == productName(event.xdata)]['Release Date'][0]
                    top = tip='Product: %s\nRelease Date: %s\nStock Price Difference: $%.2f' % (productName(event.xdata),self.dataFrame[self.dataFrame.index == productName(event.xdata)]['Release Date'][0], self.dataFrame[self.dataFrame.index == productName(event.xdata)]['Individual Stock Difference'][0] )
                    self.tooltip.SetTip(tip) 
                    self.tooltip.Enable(True)
                    collisionFound = True
                    break
        if not collisionFound:
            self.tooltip.Enable(False)

datahash = getProductReleasesForApple()

timeline = datahash

sortedTimeline = sorted(timeline.items(),key=lambda tup: tup[1][0].numericDate())

productName = []
family = []
releaseDate = []
discontinueDate = []

for item in sortedTimeline:
    # print "%s %s %s %s" % (item[0], item[1][0], item[1][1], item[1][2])
    productName.append(item[0])
    releaseDate.append(item[1][0])
    family.append(item[1][1])
    discontinueDate.append(item[1][2])

import pandas 
timelineDataFrame = pandas.DataFrame({'Product Name': productName, 'Release Date':releaseDate, 
                                    'Family': family,  'Date Discontinued': discontinueDate, 
                                    'Individual Stock Difference': 0, 'Range Stock Difference': 0, 
                                    'Stock Slope Change': 0}).set_index('Product Name')

def removeOldItems(borderDate):
    criterion = timelineDataFrame['Release Date'].map(lambda date: date.numericDate() > borderDate.numericDate())
    return timelineDataFrame[criterion]

earliestDate = Date("9-2-1985")
timelineDataFrame = removeOldItems(earliestDate)

# sampleQuery = Query("timerange", (Date("1-1-1911"), Date("3-6-1992")))
# sampleQuery.plotSlopeChanges()

sampleFamilyQuery = Query("family", 'Drives')
sampleFamilyQuery.plotIndividualStockDifferences()

# print timelineDataFrame['Macintosh plus (Platinum)']