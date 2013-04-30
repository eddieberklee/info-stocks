from bs4 import BeautifulSoup
import urllib2

opener = urllib2.build_opener()
resource = opener.open("http://apps.shareholder.com/sec/viewerContent.aspx?companyid=AAPL&docid=1199756")
data = resource.read()
resource.close()

soup = BeautifulSoup(data)
preTables = soup.findAll('pre')
financialTables = preTables[1:] # skip first table

firstTableStr = str(financialTables[0])

newLineSplit = firstTableStr.split('\n')
print newLineSplit
