#!/usr/bin/python

import cgi, cgitb

import csv

import sys

cgitb.enable()

print 'Content-Type: text/html\n'
print


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
   
    try:
        uniques = uniques + [uniques.pop(uniques.index('N/A'))]
    except ValueError:
        uniques = uniques
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
filter = pivotValues['filter']
filterValue = pivotValues['filterValue']

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
test = []
outputRow = uniqueonly(datalist[rowAttribute])
outputCol = uniqueonly(datalist[colAttribute])

#Applies filter
if filter == colAttribute:
    if filterValue not in outputCol:
        if filterValue == 'None':
            print '<h2>Need to input filter value.</h2>'
            sys.exit()
    deleteList = []
    for header in outputCol:
        if header != filterValue:
            deleteList.append(header)
    for item in deleteList:
        outputCol.remove(item)
if filterValue not in outputCol and filterValue != 'None' and filter != 'all':
    print '<h2>Filtered column does not exist.</h2>'
    sys.exit()


#Creates the aggregate count value in the form of a list
total = []
for row in outputRow:
    for col in outputCol:
        count = 0
        for item in characters:
            if item[rowAttribute] == row and item[colAttribute] == col:
                count += 1
        total.append(count)
        
# Color Function
def color(x):
    n = float(x)/float(max(total)) 
    h = 120
    s = 100
    l = 65
    a = n*1
    color = 'hsla(%s, %s%%, %s%%, %s)' % (h, s, l, a)
    return color
    
#Python Output
print '<table><tr><td></td>'

for x in outputCol:
    print '<td>%s</td>' % x
    
i = 0
for row in outputRow:
    print '<tr>'
    print '<td>%s</td>' % row
    for col in outputCol:
        print '<td style = "background-color:%s;color:black">' % color(total[i])
        print total[i]
        i += 1
        print '</td>'
    print '<tr>'

    
print '</tr>'
print '</table></body></html>'