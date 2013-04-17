import urllib
import re

class Date:
    # TODO: parse month-day-year
    pass

class Company:
    def __init__(self, name):
        self.name = name
        self.companyToSymbol() # sets self.symbol
        self.releaseDates() # sets self.releaseDates
    def __str__(self):
        return str(self.__dict__.keys())
    def companyToSymbol(self):
        url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=%s&callback=YAHOO.Finance.SymbolSuggest.ssCallback" % self.name
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
appleCompany = Company("Apple")

# TODO: enclose this into a method
productDate = appleCompany.release_dates['iBooks Author']
stockSymbol = appleCompany.symbol
smonth = 1
sday = 12
syear = 2012
emonth = 1
eday = 26
eyear = 2012
url = "http://ichart.yahoo.com/table.csv?s=%s&a=%i&b=%i&c=%i&d=%i&e=%i&f=%i&g=d&ignore=.csv" % ( stockSymbol, smonth, sday, syear, emonth, eday, eyear)
u = urllib.urlopen(url)
for perDay in u.readlines():
    print perDay.strip()

print appleCompany




