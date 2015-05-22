#!/usr/bin/python

import cgi, cgitb

cgitb.enable()

#the cgi library gets vars from html
form = cgi.FieldStorage()

pivotValues = {}

for header in form.keys():
    pivotValues[header] = form.getvalue(header)

if 'filterValue' not in pivotValues:
    pivotValues['filterValue'] = 'None'
    
print "Content-Type: text/html"
print

#Python Output
print '''<p>%s, %s, %s, %s, %s</p>''' % (pivotValues['row'], pivotValues['column'], pivotValues['value'], pivotValues['filter'], pivotValues['filterValue'])  