import pandas
import matplotlib as plt

timeline = {}

timeline['iPod'] = ['iPod Family', '12-12-12', 25]
timeline['iPod Touch'] = ['iPod Family', '1-1-1', 11]
timeline['iPhone'] = ['iPhone', '2-12-12', 100]
timeline['iMac'] = ['iMacs', '1-1-91', -25]


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