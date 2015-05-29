#!/usr/bin/python

import cgi, cgitb

import csv

import sys

import json


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
    n = float(x)/float(max(colourValues))
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

if 'filterValues[]' not in pivotValues:
    pivotValues['filterValues[]'] = 'None'

rowAttribute = pivotValues['row']
colAttribute = pivotValues['column']
value = pivotValues['value']
filterValues = pivotValues['filterValues[]']
wantFilter = pivotValues['wantFilter']

file = open('./data/combined.csv',"rU")
reader = csv.DictReader(file)

datalist = {title.strip().lower():[data.strip()]
            for title, data in reader.next().items()}


characters = [] #A list, where each item will be a dictionary for each character
totalCharacters = 0
totalAppearances = 0

for row in reader:
    totalCharacters += 1
    characters.append(row)
    for title, data in row.items():
        title = title.strip()
        datalist[title].append(data.strip())

for character in characters:
    #Replaces any empty values with "N/A"
    for header, count in character.iteritems():
        if not count and header == "appearances":
            character[header] = 0
        elif not count:
            character[header] = "N/A"
    totalAppearances += int(character["appearances"])


###############################################################################
#GENERATION OF PROCESSED DATA
###############################################################################

#Determine row and column to output
outputRow = uniqueonly(datalist[rowAttribute])
outputCol = uniqueonly(datalist[colAttribute])

#Determines if the python script is being used to generate the pivot table or filter columns
if wantFilter == "True":
    print 'Content-Type: application/json'
    print
    print json.dumps(outputCol)
    sys.exit()
else:
    print 'Content-Type: text/html\n'
    print
                         

#Applies filters and also checks for error handling
if type(filterValues) == list:
    for filterValue in filterValues:
        if filterValue not in outputCol and filterValue != 'None':
            print '<h2>A chosen filtered column does not exist.</h2>'
            sys.exit()

if filterValues != 'None':
    deleteList = []
    for header in outputCol:
        if header not in filterValues:
            deleteList.append(header)
    for item in deleteList:
        outputCol.remove(item)

if rowAttribute == colAttribute:
    print '<h2>Having the same column and row is not recommended, but alright.</h2>'

#Creates the aggregate count value in the form of a list
tableValues = []
colourValues = [] #Used to calculate the colour of each cell
percentValue = 0

if value == "appearances" or value == "appearancesPercent":
    for row in outputRow:
        for col in outputCol:
            count = 0
            for item in characters:
                if item[rowAttribute] == row and item[colAttribute] == col:
                    count += int(item["appearances"])
            tableValues.append(count)
            if value == "appearancesPercent":
                colourValues.append(float(count)/totalAppearances * 100)
            else:
                colourValues.append(count)
        #Calculates the sum of each row.
        tableValues.append(sum(tableValues[-(len(outputCol)):]))    
else: #Count and count percent
    for row in outputRow:
        for col in outputCol:
            count = 0
            for item in characters:
                if item[rowAttribute] == row and item[colAttribute] == col:
                    count += 1
            tableValues.append(count)
            if value == "percent":
                colourValues.append(float(count)/totalCharacters * 100)
            else:
                colourValues.append(count)
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
elif value == "appearancesPercent":
    i = 0
    for item in tableValues:
        percentValue = round(float(item)/totalAppearances * 100, 2)
        tableValues[i] = percentValue
        i += 1



###############################################################################
#DATA OUTPUT
###############################################################################
                         
print '<table id="actualTable"><tr><td></td>'

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
print '</tr></table>'

#Printing of the Colour Gradient Legend
if value == "count" or value == "appearances":
    print '''
        <h3>Colour Legend</h3>
        <table><tr><td id="gradientCell"></td></tr></table>
        <p style="margin-top: -1.5em">Min: %s<span style="float: right">Max: %s</p></body></html>
        ''' % (min(colourValues), max(colourValues))
else:
    print '''
        <h3>Colour Legend</h3>
        <table><tr><td id="gradientCell"></td></tr></table>
        <p style="margin-top: -1.5em">Min: %s%%<span style="float: right">Max: %s%%</p></body></html>
        ''' % (round(min(colourValues),2), round(max(colourValues),2))