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
        

#Pie Chart 1: Sorting alignments by gender
goodFemale = badFemale = neutralFemale = reformedFemale = 0
goodMale = badMale = neutralMale = reformedMale = 0
list = []
for x in characters:
    if x['sex'] == 'Female Characters':
        if x['align'] == 'Good Characters':
            goodFemale += 1
        elif x['align'] == 'Neutral Characters':
            neutralFemale += 1
        elif x['align'] == 'Bad Characters':
            badFemale += 1           
        elif x['align'] == 'Reformed Criminals':
            reformedFemale += 1
    elif x['sex'] == 'Male Characters':
        if x['align'] == 'Good Characters':
            goodMale += 1
        elif x['align'] == 'Neutral Characters':
            neutralMale += 1
        elif x['align'] == 'Bad Characters':
            badMale += 1           
        elif x['align'] == 'Reformed Criminals':
            reformedMale += 1

dataset['alignPieData'] = {"goodFemale": goodFemale, "badFemale": badFemale,
                           "neutralFemale": neutralFemale, "reformedFemale": reformedFemale,
                           "goodMale": goodMale, "badMale": badMale,
                           "neutralMale": neutralMale, "reformedMale": reformedMale}


print 'Content-Type: application/json'
print

print json.dumps(dataset)