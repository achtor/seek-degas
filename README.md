# seekdegas

This is a simple library for scraping the SEC's EDGAR resource. Companies like <a href="https://seekinf.co">seekinf</a> charge for full access to the data, despite it being free on their FTP server.

Feel free to contribute; there is quite a bit of functionality that is still missing. Some of it is because I don't have enough experience with the data to know what's going on with it.

Immediate TODO list:
- Implement XBRL search functionality - not actually sure what this is yet.
- Keyphrase search is incredibly slow right now due to the necessity of opening and searching each individual text file from the FTP server, but the commercial resource mentioned above shows that it doesn't have to be slow - figure out how to change this. 
- Make availability of the output in other formats part of the library - downloading a CSV, etc. Downloading the archival files made available by the SEC may also be useful.
- Allow filtering by finer timeframes than entire years. Quarters at the least; are individual days necessary/useful?
- Create a web interface for easy use.

SIC lookup data gleaned from the results of <a href="https://github.com/mattkiefer/sec-sic-scraper/blob/master/scraper.py">Matt Kiefer's scraper</a>.
