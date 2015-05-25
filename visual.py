import re
import csv
import json
from collections import defaultdict

reader=csv.DictReader(open('./data/combined.csv',"rU"))

datalist = {title.strip():[data.strip()]
            for title, data in reader.next().items()}

#A dictionary to store all the output data
dataset = defaultdict()

#A list, where each item will be a dictionary for each character
characters = []

for row in reader:
    characters.append(row)
    for title, data in row.items():
        title = title.strip()
        datalist[title].append(data.strip())

for character in characters:
    #Replaces any empty values with "N/A"
    for header, count in character.iteritems():
        if not count:
            character[header] = "N/A"
        

#Pie Chart 1 and 2: Sorting alignments by gender
goodFemale = badFemale = neutralFemale = reformedFemale = 0
goodMale = badMale = neutralMale = reformedMale = 0

#Stacked Chart: Gender Ratio by Year
maleCount =  defaultdict(int)
femaleCount = defaultdict(int)
totalCount = defaultdict(int)

#Bar Chart for Gender Count
totalMale = totalFemale = total = 0

for x in characters:
    totalCount[x['year']] += 1
    total += 1
    if x['sex'] == 'Female Characters':
        femaleCount[x['year']] += 1
        totalFemale += 1
        if x['align'] == 'Good Characters':
            goodFemale += 1
        elif x['align'] == 'Neutral Characters':
            neutralFemale += 1
        elif x['align'] == 'Bad Characters':
            badFemale += 1           
        elif x['align'] == 'Reformed Criminals':
            reformedFemale += 1
    elif x['sex'] == 'Male Characters':
        totalMale += 1
        maleCount[x['year']] += 1
        if x['align'] == 'Good Characters':
            goodMale += 1
        elif x['align'] == 'Neutral Characters':
            neutralMale += 1
        elif x['align'] == 'Bad Characters':
            badMale += 1           
        elif x['align'] == 'Reformed Criminals':
            reformedMale += 1

#Pie Chart 1 and 2
dataset['alignPieData'] = {"goodFemale": goodFemale, "badFemale": badFemale,
                           "neutralFemale": neutralFemale, "reformedFemale": reformedFemale,
                           "goodMale": goodMale, "badMale": badMale,
                           "neutralMale": neutralMale, "reformedMale": reformedMale}

#Stacked Chart
femaleCount.pop('N/A')
maleCount.pop('N/A')
totalCount.pop('N/A')

for year in maleCount.keys():
    if year not in femaleCount.keys():
        femaleCount[year] = 0
for year in femaleCount.keys():
    if year not in maleCount.keys():
        maleCount[year] = 0

dataset['femaleCount'] = femaleCount
dataset['maleCount'] = maleCount
dataset['totalCount'] = totalCount

#Generates a cumulative total for each gender year-by-year
cumulativeMale = [1]
cumulativeFemale = [0] #There were 0 female characters in the first year
cumulativeTotal = [1]
i = 0
for year in sorted(maleCount.keys()):
    #Males and females should have the same number of years due to the for loops earlier
    cumulativeMale.append(cumulativeMale[i] + maleCount[year])
    cumulativeFemale.append(cumulativeFemale[i] + femaleCount[year])
    
    #Don't want to sum cumulativeMale with cumulativeFemale to get the total amount of characters that
    #were given a valid year in the dataset. This is because genders include more than just males and females.
    cumulativeTotal.append(cumulativeTotal[i] + totalCount[year])
    i += 1
    
dataset['cumulativeMale'] = cumulativeMale
dataset['cumulativeFemale'] = cumulativeFemale
dataset['cumulativeTotal'] = cumulativeTotal


#Bar Chart for Gender Count
totalOthers = total - (totalMale + totalFemale)
dataset['genderCount'] = {"totalMale": totalMale, "totalFemale": totalFemale, "totalOthers": totalOthers, "total": total}
        

#Scatterplot data 
#a dictionary with count of public identities for each year
publicCount = defaultdict(float)
#a dictionary with ratio of public identities for each year
publicRatio = defaultdict(float)

for x in characters:
    if x['id'] == 'Public Identity':
        publicCount[x['year']] += 1 
        
        
for year in publicCount:
    for year2 in totalCount:
        if year == year2:
            publicRatio[year] = publicCount[year]/totalCount[year]
            
goodCount = defaultdict(float)
goodRatio = defaultdict(float)

for x in characters:
    if x['align'] == 'Good Characters':
        goodCount[x['year']] += 1
        
for year in goodCount:
    for year2 in totalCount:
        if year == year2:
            goodRatio[year] = goodCount[year]/totalCount[year]
            
#Format accepted by scatterplot is listoflists
scatterPlotData = []
list = []

for year in publicRatio:
    for year2 in goodRatio:
        if year == year2:
            scatterPlotData.append([goodRatio[year],publicRatio[year]])
    

            
dataset['scatterPlotData'] = scatterPlotData
            

        


#Output
print 'Content-Type: application/json'
print

print json.dumps(dataset)