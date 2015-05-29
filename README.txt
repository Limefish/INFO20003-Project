How to Run:
	Serve 'index.html', which should load up the home page.

Dataset:
	Dataset originally consisted of two files and separated by their comic publisher. These two CSV files were then merged
	into a single csv file, making the publisher a new column. Certain attributes were also removed from the dataset
	as they were more 'metadata' than actual data, e.g. the URL for the wiki page of that character.

	Dataset was rather limiting due to most attributes being categorical and discrete rather than numerical and continuous.
	
	Credits for the dataset provided in the webpage footer.

Files:
	A HTML and CSS template was used in order to save time, where it was then modified to fit our requirements.
	Credits for the template is provided in the webpage footer.
	
	Files that were entirelly written from stratch are pivot.py, pivot.js, visual.py, visual.js, while a few other files were modified.

Technologies and Libraries:
	Highcharts was used to visualise the data, where the data itself was processed by Python and outputted as one JSON file.

	JavaScript and jQuery was used to mediate the data between the HTML pages and the Python backend.

	jQuery Tokenize was used to create the multi-select dropdown in the Pivot Table.

Note: 
	'Auburn Hair' is considered an Eye Colour by the dataset for some reason, so it's not actually a data processing error.

	'Stretch goals.txt' contains a few goals that couldn't be achieved in time.