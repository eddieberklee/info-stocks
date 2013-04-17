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
    def dateRange(self, range): # range is in days
        import datetime
        date = datetime.date(int(self.y), int(self.m), int(self.d))
        
        difference = datetime.timedelta(days=range)
        beginInterval = date - difference
        endInterval = date + difference

        beginInterval = str(beginInterval.month) + '-' + str(beginInterval.day) + '-' + str(beginInterval.year)
        endInterval = str(endInterval.month) + '-' + str(endInterval.day) + '-' + str(endInterval.year)

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
    def getData(self):
        productDate = Date(self.release_dates['Apple TV (3rd gen)'])
        dateRange = productDate.dateRange(7)
        startDate = dateRange[0]
        endDate = dateRange[1]
        interval = 'd'
        url = "http://ichart.yahoo.com/table.csv?s=%s&a=%i&b=%i&c=%i&d=%i&e=%i&f=%i&g=%s&ignore=.csv" \
            % ( self.symbol, startDate.m-1, startDate.d, startDate.y, endDate.m-1, endDate.d, endDate.y, interval)
        u = urllib.urlopen(url)
        ulines = u.read().split("\n")
        start = ulines[1]
        end = ulines[-2]
        print 'Legend:             ' + ulines[0]
        print 'Starting Date Data: ' + start
        print 'Ending Date Data:   ' + end
        difference = parse_yahoo_stock(start)['Close'] - parse_yahoo_stock(end)['Close']
        if difference > 0:
            sign = '+'
        else:
            sign = '-'
        print sign + ' ' + str(difference)
        # for perDay in u.readlines():
        #     print perDay.strip()


apple = Company("Apple")
apple.getData()

