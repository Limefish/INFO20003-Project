import re
import csv
import json
from collections import defaultdict

###############################################################################
#Data Import and Initial Processing
###############################################################################
reader=csv.DictReader(open('./data/combined.csv',"rU"))

#A dictionary, where each variable is a key
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

#Sexual and Gender Minority
totalHomo = totalBi = totalHetero = totalOthers = 0
goodHomo = badHomo = neutralHomo = 0
goodBi = badBi = neutralBi = 0
goodHetero = badHetero = neutralHetero = 0
homoCount =  defaultdict(int)
heteroCount = defaultdict(int)
biCount = defaultdict(int)

for x in characters:
    totalCount[x['year']] += 1
    total += 1

    #Generates count of alignments by Gender
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
    
    #Generates count of alignments by Sexual Orientation
    if x['gsm'] == 'Homosexual Characters':
        homoCount[x['year']] += 1
        totalHomo += 1
        if x['align'] == 'Good Characters':
            goodHomo += 1
        elif x['align'] == 'Neutral Characters':
            neutralHomo += 1
        elif x['align'] == 'Bad Characters':
            badHomo += 1           
    elif x['gsm'] == 'N/A':
        #Assumes that those not labelled as a sexual minority by the dataset are straight
        heteroCount[x['year']] += 1
        totalHetero += 1
        if x['align'] == 'Good Characters':
            goodHetero += 1
        elif x['align'] == 'Neutral Characters':
            neutralHetero += 1
        elif x['align'] == 'Bad Characters':
            badHetero += 1           
    elif x['gsm'] == 'Bisexual Characters':
        biCount[x['year']] += 1
        totalBi += 1
        if x['align'] == 'Good Characters':
            goodBi += 1
        elif x['align'] == 'Neutral Characters':
            neutralBi += 1
        elif x['align'] == 'Bad Characters':
            badBi += 1 
    else:
        totalOthers += 1



###############################################################################
#Pie Chart 1 and 2
###############################################################################
dataset['alignPieData'] = {"goodFemale": goodFemale, "badFemale": badFemale,
                           "neutralFemale": neutralFemale, "reformedFemale": reformedFemale,
                           "goodMale": goodMale, "badMale": badMale,
                           "neutralMale": neutralMale, "reformedMale": reformedMale}


###############################################################################
#Stacked Chart
###############################################################################
maleYear = []
maleValue = []
femaleYear = []
femaleValue = []

femaleCount.pop('N/A')
maleCount.pop('N/A')
totalCount.pop('N/A')

for year in maleCount.keys():
    if year not in femaleCount.keys():
        femaleCount[year] = 0
for year in femaleCount.keys():
    if year not in maleCount.keys():
        maleCount[year] = 0

for year in sorted(maleCount.keys()):
    #Males and females should have the same number of years due to the for loops earlier
    maleYear.append(year)
    maleValue.append(float(maleCount[year])/totalCount[year])
    femaleYear.append(year)
    femaleValue.append(float(femaleCount[year])/totalCount[year])

#Generates a cumulative total for each gender year-by-year
cumulativeMale = [1]
cumulativeFemale = [0] #There were 0 female characters in the first year
cumulativeTotal = [1]
i = 0
for year in maleYear[1:]:
    cumulativeMale.append(cumulativeMale[i] + maleCount[year])
    cumulativeFemale.append(cumulativeFemale[i] + femaleCount[year])
    #Don't want to sum cumulativeMale with cumulativeFemale to get the total amount of characters that
    #were given a valid year in the dataset. This is because genders include more than just males and females.
    cumulativeTotal.append(cumulativeTotal[i] + totalCount[year])
    i += 1

for year in range(len(maleYear)):
    cumulativeMale[year] = (float(cumulativeMale[year])/cumulativeTotal[year])
    cumulativeFemale[year] = (float(cumulativeFemale[year])/cumulativeTotal[year])

dataset['genderYear'] = {'maleYear': maleYear, 'maleValue': maleValue,
                          'femaleYear': femaleYear, 'femaleValue': femaleValue,
                          'cumulativeMale': cumulativeMale, 'cumulativeTotal': cumulativeTotal,
                          'cumulativeFemale': cumulativeFemale}


###############################################################################
#Bar Chart for Gender Count
###############################################################################
totalOthers = total - (totalMale + totalFemale)
dataset['genderCount'] = {"totalMale": totalMale, "totalFemale": totalFemale, "totalOthers": totalOthers, "total": total}

        
###############################################################################
#Column Chart for Sexual Orientation
###############################################################################
homoRatios = {'good': round(float(100*goodHomo)/totalHomo, 2),
              'neutral': round(float(100*neutralHomo)/totalHomo, 2),
              'bad': round(float(100*badHomo)/totalHomo, 2)}

biRatios = {'good': round(float(100*goodBi)/totalBi, 2),
            'neutral': round(float(100*neutralBi)/totalBi, 2),
            'bad': round(float(100*badBi)/totalBi, 2)}

heteroRatios = {'good': round(float(100*goodHetero)/totalHetero, 2),
              'neutral': round(float(100*neutralHetero)/totalHetero, 2),
              'bad': round(float(100*badHetero)/totalHetero, 2)}

dataset['orientationAlign'] = {"totalHomo": totalHomo, "totalHetero": totalHetero, "totalBi": totalBi, "totalOthers" : totalOthers,
                               "homo": homoRatios, "bi": biRatios, "hetero": heteroRatios}

"""
dataset['orientationAlign'] = {"totalHomo": totalHomo, "totalHetero": totalHetero, "totalBi": totalBi, "totalOthers" : totalOthers,
                               "goodHomo": goodHomo, "neutralHomo": neutralHomo, "badHomo": badHomo,
                               "goodHetero": goodHetero, "neutralHetero": neutralHetero, "badHetero": badHetero,
                               "goodBi": goodBi, "neutralBi": neutralBi, "badBi": badBi}
"""

###############################################################################
#Column Chart for Sexual Orientation
###############################################################################
homoYear = []
homoValue = []
biYear = []
biValue = []
heteroYear = []
heteroValue = []

homoCount.pop('N/A')
heteroCount.pop('N/A')

for year in maleCount.keys():
    if year not in homoCount.keys():
        homoCount[year] = 0
    if year not in heteroCount.keys():
        heteroCount[year] = 0
    if year not in biCount.keys():
        biCount[year] = 0

for year in sorted(homoCount.keys()):
    homoYear.append(year)
    homoValue.append(homoCount[year])
    heteroYear.append(year)
    heteroValue.append(heteroCount[year])
    biYear.append(year)
    biValue.append(biCount[year])

dataset['orientationYear'] = {'homoYear': homoYear, 'homoValue': homoValue,
                              'heteroYear': heteroYear, 'heteroValue': heteroValue,
                              'biYear': biYear, 'biValue': biValue}


###############################################################################
#Scatterplot data 
###############################################################################

#Dictionaries for count and ratio of public identities for each year
publicCount = defaultdict(float)
publicRatio = defaultdict(float)

for x in characters:
    if x['id'] == 'Public Identity':
        publicCount[x['year']] += 1 
        
        
for year in publicCount:
    for year2 in totalCount:
        if year == year2:
            publicRatio[year] = publicCount[year]/totalCount[year]
            
#Dictionaries for count and ratio of good characters for each year            
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
            scatterPlotData.append({'year':year, 'x':goodRatio[year], 'y':publicRatio[year]})
                
dataset['scatterPlotData'] = scatterPlotData
            

###############################################################################
#Output
###############################################################################
print 'Content-Type: application/json'
print

print json.dumps(dataset)