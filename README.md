# TwitterWordMining
Mines Twitter for terms and creates a simple proof of concept summary statistics

## Source files
### Scraper.py -- Used to scrape tweets via twitter API, perform a sentiment analysis, and store results in a database

Non-Standard Python Modules Required:
	- pip install Tweepy
	- pip install NLTK
	- pip install TextBlob
		
How to Run:
	>python Scraper.py
	note: It will create a new database named IT_Vendors_Terms.db in the current directory if the current directory does not contain the database already. If the database is in the current directory it will proceed to update it with new information
	
### Database.py -- Used to set up a sqlite3 database and provide an interface to it for Scraper.py

How to Run:
	Will automatically be used by Scraper.py, but must be in the same folder as Scraper.py


### Analyzer.py -- Used to querry database a present a few interesting summaries

Non-Standard Python Modules Required:
	- pip install Pandas

How to Run:
	python Analyzer.py <path to database>
	e.g.: >python Analyzer.py IT_Vendors_Terms.db
