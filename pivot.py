#!/usr/bin/python

import cgi, cgitb

import csv

cgitb.enable()

# Function to obtain a list of uniques
def uniqueonly(x):
    uniques = []
    setlist = set(x)
    for item in setlist:
        if not item:
            #Gives empty cells within the csv a value of 'N/A'
            item = 'N/A'
        uniques.append(item)
    uniques = sorted(uniques)
    uniques = uniques + [uniques.pop(uniques.index('N/A'))]
    return uniques

#the cgi library gets vars from html
form = cgi.FieldStorage()

pivotValues = {}

for header in form.keys():
    pivotValues[header] = form.getvalue(header)

if 'filterValue' not in pivotValues:
    pivotValues['filterValue'] = 'None'

rowAttribute = pivotValues['row']
colAttribute = pivotValues['column']

file = open('./data/combined.csv',"rU")
reader = csv.DictReader(file)

datalist = {title.strip().lower():[data.strip()]
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
        
#Determine row and column to output
outputRow = uniqueonly(datalist[rowAttribute])
outputCol = uniqueonly(datalist[colAttribute])

#Creates the aggregate count value in the form of a list
total = []
for row in outputRow:
    for col in outputCol:
        count = 0
        for item in characters:
            if item[rowAttribute] == row and item[colAttribute] == col:
                count += 1
        total.append(count)
    
#Python Output
print 'Content-Type: text/html\n'
print

print '<table><tr><td></td>'

for x in outputCol:
    print '<td>%s</td>' % x
    
i = 0
for row in outputRow:
    print '<tr>'
    print '<td>%s</td>' % row
    for col in outputCol:
        print '<td>'
        print total[i]
        i += 1
        print '</td>'
    print '<tr>'

    
print '</tr>'
print '</table></body></html>'