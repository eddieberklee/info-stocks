import urllib
import re

class Date:
    def __init__(self, date):
        splitDate = date.split('-')

        self.date = date
        self.m = splitDate[1]
        self.d = splitDate[0]
        self.y = splitDate[2]

    # returns a tuple of start date and beginning date
    def dateRange(self, range): # range: num days
        import datetime
        date = datetime.date(int(self.y), int(self.m), int(self.d))
        
        difference = datetime.timedelta(days=range)
        beginInterval = date - difference
        endInterval = date + difference

        beginInterval = str(beginInterval.month) + '-' + str(beginInterval.day) + '-' + str(beginInterval.year)
        endInterval = str(endInterval.month) + '-' + str(endInterval.day) + '-' + str(endInterval.year)

        return (Date(beginInterval), Date(endInterval))
        
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
        productDate = self.release_dates['iBooks Author']
        smonth = 1
        sday = 12
        syear = 2012
        emonth = 1
        eday = 26
        eyear = 2012
        url = "http://ichart.yahoo.com/table.csv?s=%s&a=%i&b=%i&c=%i&d=%i&e=%i&f=%i&g=d&ignore=.csv" \
            % ( self.symbol, smonth, sday, syear, emonth, eday, eyear )
        u = urllib.urlopen(url)
        for perDay in u.readlines():
            print perDay.strip()


apple = Company("Apple")
print apple.getData()

sampleDate = Date("1-1-2013")
print sampleDate.dateRange(80)


