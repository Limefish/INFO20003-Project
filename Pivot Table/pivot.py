import cgi
import csv

# Function to obtain a list of uniques
def uniqueonly(x):
    uniques = []
    setlist = set(x)
    for item in setlist:
        uniques.append(item) 
    return uniques

data = cgi.FieldStorage()
test= data.getfirst('row',)

file = open('testdata.csv',"rU")
reader = csv.DictReader(file)

datalist = {title.strip():[data.strip()]
            for title, data in reader.next().items()}

for row in reader:
    for title, data in row.items():
        title = title.strip()
        datalist[title].append(data.strip())

#print test

#x = uniqueonly(datalist['test'])


    
    
    
    
    
    



print '''Content-Type: text/html\n\n 
<!DOCTYPE html>
<html>
<head>
    <style>%s</style>
</head>    
<body>
<table>
    <tbody>%s</tbody>
</table>
</body>
</html>''' % (test, test)  