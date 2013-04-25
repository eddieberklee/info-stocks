import pandas
import matplotlib as plt

timeline = {}

timeline['iPod'] = ['iPod Family', Date('12-12-12'), 25]
timeline['iPod Touch'] = ['iPod Family', Date('1-1-1'), 11]
timeline['iPhone'] = ['iPhone', Date('2-12-12'), 100]
timeline['iMac'] = ['iMacs', Date('1-1-91'), -25]

for item in timeline.items():
	print item[1][1].dateSort()
#sortedTimeline = timeline.items().sort(key=lambda tup: tup[1][1].dateSort())
sortedTimeline = sorted(timeline.items(),key=lambda tup: tup[1][1].dateSort())

print sortedTimeline

productName = []
family = []
releaseDate = []
stockSlope = []

for item in sortedTimeline:
	print item
	productName.append(item[0])
	family.append(item[1][0])
	releaseDate.append(item[1][1])
	stockSlope.append(item[1][2])

timelineDataFrame = pandas.DataFrame({'Product Name': productName, 'Family': family, 'Release Date':releaseDate, 'Stock Impact': stockSlope}).set_index('Product Name')

timelineDataFrame.plot(use_index=True, y='Stock Impact')
