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
            item = 'N/A'
        uniques.append(item)
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

for row in reader:
    for title, data in row.items():
        title = title.strip()
        datalist[title].append(data.strip())


        
#determine row and column to output
outputRow = uniqueonly(datalist[rowAttribute])
outputCol = uniqueonly(datalist[colAttribute])


#Python Output
print 'Content-Type: text/html\n'
print
print '<table><tr><td></td>'

for x in outputCol:
    print '<td>%s</td>' % x
    
for x in outputRow:
    print '<tr>'
    print '<td>%s</td>' % x
    for x in outputCol:
        print '<td>'
        print 'Placeholder'
        print '</td>'
    print '<tr>'

    
print '</tr>'
print '</table></body></html>'
