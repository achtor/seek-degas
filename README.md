# seekdegas

This is a simple Python 2.7 library for scraping the SEC's EDGAR resource. Companies like <a href="https://www.seekinf.co:8443">seekinf</a> charge for full access to the data, despite it being free on their FTP server.

Right now, to use it, simply add it as a submodule (or install it in your python packages directory), and use the built-in functions <code>seekdegas.query</code> and <code>seekdegas.download</code>.

The function <code>query</code> accepts arguments <code>start,end</code>, which are integers indicating the start and end years (range since 1993), and the other arguments are all optional filters: <code>cik,sic,company</code> are all string arguments to filter for those specific fields (CIK number, SIC number, exact company name as listed on official documents case-insensitive). <code>forms</code> is a list of strings of form names (e.g. <code>['10-K','10-Q']</code> is a possible selection). <code>keyphrases</code> is a list of strings to search for in the documents, but its use is not recommended, since it makes the search extremely slow.

<code>query</code> yields an iterator of hashtables, each of which has keys <code>cik,company,form,date,url</code> all of which are fairly self-explanatory. <code>date</code> is the date listed on the filing, which might sometimes conflict with the quarter or even the year in which it was listed. <code>url</code> is the url of the text/HTML document on the FTP server with the filing.

The function <code>download</code> is the same, but it downloads the files instead of yielding the hashtables. It also accepts strings <code>regex,regopt</code>, which enable you to just download portions of the filings by extracting using regular expressions - these are fed directly into <code>re.findall</code>; see the <a href="http://docs.python.org/2/library/re.html">re package documentation</a> for more information. <code>filepath</code> is the name of the folder you want to save these into, no backslashes - it's a relative path, so it'll simply save them into that subdirectory of wherever you're running the script. <code>fileprefix</code> will add that string to the beginning of each of the filenames as they're saved. The base name format is (CIK number)-(date of filing).txt.

You can create your own functions with the <code>@edgar</code> decorator. It feeds the wrapped function a single variable <code>fdata</code>, which is an array containing the CIK number, company name, form name, date of filing, and URL of filing on the server (without the domain), in that order, indexed from 0. Arguments taken by the wrapped function are then identical to those of the function <code>query</code>. The decorator iterates through and yields the results of the wrapped function for every filing matched under those parameters; functions returning nothing but simply performing an action (for example, <code>download</code>) are fine as well. If you want further arguments, those work fine as well as long as they're named arguments with defaults - the implementation is using <code>**kwargs</code> See the source code for details. 

Keyphrase search is incredibly slow right now due to the necessity of opening and searching each individual text file from the FTP server, but the commercial resource mentioned above shows that it doesn't have to be slow - figure out how to change this. 

Feel free to contribute; there is quite a bit of functionality that is still missing. Some of it is because I don't have enough experience with the data to know what's going on with it.

Immediate TODO list:
- Implement XBRL search functionality - not actually sure what this is yet.
- Make availability of the output in other formats part of the library - downloading a CSV, etc. Downloading the archival files made available by the SEC may also be useful.
- Allow filtering by finer timeframes than entire years. Quarters at the least; are individual days necessary/useful?
- Create a web interface for easy use.

SIC lookup data gleaned from the results of <a href="https://github.com/mattkiefer/sec-sic-scraper/blob/master/scraper.py">Matt Kiefer's scraper</a>.
