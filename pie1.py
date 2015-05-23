import cgi
import csv
import cgitb; cgitb.enable()
import re
import csv
import json

reader=csv.DictReader(open('./data/combined.csv',"rU"))

datalist = {title.strip():[data.strip()]
            for title, data in reader.next().items()}
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
            
            
#counting female(not really needed)            
femalecount = 0            
for x in characters:
    if x['sex'] == 'Female Characters':
        femalecount += 1

        

#counting female with good or bad alignment

goodfemale = 0
badfemale = 0
neutralfemale = 0
reformedfemale = 0
notavailable = 0
list = []
for x in characters:
    if x['sex'] == 'Female Characters':
        if x['align'] == 'Good Characters':
            goodfemale += 1
        elif x['align'] == 'Neutral Characters':
            neutralfemale += 1 
        elif x['align'] == 'Bad Characters':
            badfemale += 1           
        elif x['align'] == 'Reformed Criminals':
            reformedfemale += 1
        else: 
            notavailable += 1


alignpiedata = {"goodfemale": goodfemale, "badfemale": badfemale, "neutralfemale": neutralfemale, "reformedfemale": reformedfemale, "notavailable": notavailable}

print alignpiedata
            
            


