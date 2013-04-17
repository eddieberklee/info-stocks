
class Company:
    def __init__(self, name):
        self.name = name
        self.companyToSymbol() # sets self.symbol
    def __str__(self):
        return str(self.__dict__.keys())
    def companyToSymbol(self):
        import urllib
        import re
        url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=%s&callback=YAHOO.Finance.SymbolSuggest.ssCallback" % self.name
        u = urllib.urlopen(url)
        data = u.read()
        m = re.search('symbol\":\"[a-zA-Z]*\"', data)
        symbol = m.group(0)
        symbol = symbol.split(':')[1][1:-1]
        self.symbol = symbol
        return symbol
appleCompany = Company("Apple")
print appleCompany




