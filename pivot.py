#!/usr/bin/python

import cgi, cgitb

import csv

import sys

cgitb.enable()

print 'Content-Type: text/html\n'
print


###############################################################################
#FUNCTIONS
###############################################################################

#Function to obtain a list of unique values and assigns empty cells within the
#CSV a value of 'N/A'
def uniqueonly(x):
    uniques = []
    setlist = set(x)
    for item in setlist:
        if not item:
            item = 'N/A'
        uniques.append(item)
    uniques = sorted(uniques)

    try:
        #For cases when there is no empty cells within the data
        uniques = uniques + [uniques.pop(uniques.index('N/A'))]
    except ValueError:
        uniques = uniques
    return uniques

#Used to colour the cells of the pivot table,
#where colour varies with the cell's value
def color(x):
    n = float(x)/float(max(tableValues))
    if n <= 0.5:
        r = 239
        g = 138
        b = 98
        a = 1-(n*2)
    else:
        r = 103
        g = 169
        b = 207
        a = (n-0.5)*2
    color = 'rgba(%s, %s, %s, %s)' % (r, g, b, a)
    return color


###############################################################################
#DATA AND CGI IMPORT
###############################################################################

#The cgi library gets vars from the select fields in the html page.
form = cgi.FieldStorage()

pivotValues = {}

for header in form.keys():
    pivotValues[header] = form.getvalue(header)

if 'filterValue' not in pivotValues:
    pivotValues['filterValue'] = 'None'

rowAttribute = pivotValues['row']
colAttribute = pivotValues['column']
value = pivotValues['value']
filter = pivotValues['filter']
filterValue = pivotValues['filterValue']

file = open('./data/combined.csv',"rU")
reader = csv.DictReader(file)

datalist = {title.strip().lower():[data.strip()]
            for title, data in reader.next().items()}


#A list, where each item will be a dictionary for each character
characters = []
totalCharacters = 0

for row in reader:
    totalCharacters += 1
    characters.append(row)
    for title, data in row.items():
        title = title.strip()
        datalist[title].append(data.strip())

for character in characters:
    #Replaces any empty values with "N/A"
    for header, count in character.iteritems():
        if not count:
            character[header] = "N/A"


###############################################################################
#GENERATION OF PROCESSED DATA
###############################################################################

#Determine row and column to output
outputRow = uniqueonly(datalist[rowAttribute])
outputCol = uniqueonly(datalist[colAttribute])

#Applies filters and also checks for error handling
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
if outputRow == outputCol:
    print '<h2>Having the same column and row is not recommended, but alright.</h2>'

#Creates the aggregate count value in the form of a list
tableValues = []
percentValue = 0

for row in outputRow:
    for col in outputCol:
        count = 0
        for item in characters:
            if item[rowAttribute] == row and item[colAttribute] == col:
                count += 1
        tableValues.append(count)
    #Calculates the sum of each row.
    tableValues.append(sum(tableValues[-(len(outputCol)):]))

#Calculates the sum of each column
for column in range((len(outputCol)+1)):
    tableValues.append(sum(tableValues[column::(len(outputCol)+1)]))
    

if value == "percent":
    #Returns values as percentages instead of aggreate count
    i = 0
    for item in tableValues:
        percentValue = round(float(item)/totalCharacters * 100, 2)
        tableValues[i] = percentValue
        i += 1


###############################################################################
#DATA OUTPUT
###############################################################################

print '<table><tr><td></td>'

for x in outputCol:
    print '<td>%s</td>' % x
print '<td><b>Total</b></td>'    
    
i = 0
for row in outputRow:
    print '<tr>'
    print '<td style="background-color: rgba(144, 144, 144, 0.075)">%s</td>' % row
    for col in outputCol:
        print '<td style = "background-color:%s;color:black">' % color(tableValues[i])
        print tableValues[i]
        i += 1
        print '</td>'
    #Prints Row Total
    print '<td style="background-color: rgba(144, 144, 144, 0.075); text-align: right"><b>%s</b></td>' % tableValues[i]
    i += 1
    print '<tr>'

#Printing of Column Total
print '</tr><tr>'
print '<td style="background-color: rgba(144, 144, 144, 0.075)"><b>Total</b></td>' 
for column in range((len(outputCol)+1)):
    position = len(outputCol) + 1 - column
    if position == 1:
        print '<td style="background-color: rgba(144, 144, 144, 0.075); text-align: right"><b>%s</b></td>' % tableValues[-(position)]
    else:
        print '<td style="background-color: rgba(144, 144, 144, 0.075)"><b>%s</b></td>' % tableValues[-(position)]
print '</tr>'

print '</table></body></html>'