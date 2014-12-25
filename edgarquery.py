import urllib2
from datetime import date
from .sic import sicIndex

"""
Function query takes in:
 - start, a numerical year since 1993. Defaults to 1993.
 - end, a numerical year between start and the present year.
 - form, a list of strings of form types to search for. (See list of form-types) Defaults
   to None, in which case all forms are searched for.
 - company, the desired company exact name (no punctuation, case-insensitive), as a string.
   Defaults to none, in which case all companies are searched for.
 - cik, the desired CIK number as a string. Defaults to None, in which case all CIK numbers 
   are searched for.
 - sic, the desired SIC number as a string. Defaults to None, in which case all SIC numbers
   are searched for.
 - keyphrases, a list of strings of exact phrases to search for
"""
def query(start = 1993, end = int(date.today().year), forms = None, company = None,
               cik = None, sic = None, keyphrases = None):
   # list of results
   results = []

   # Cycle through all the FTP holdings between the two dates
   for year in range(start, end + 1):
      for q in range(1,5):
         print 'Year ' + str(year) + ' quarter ' + str(q)
         try:
            f = urllib2.urlopen('ftp://ftp.sec.gov/edgar/full-index/' + str(year) + '/QTR' 
                                 + str(q) + '/master.idx')
         except Exception,e:
            print str(e)
            return # Out of range? Move on
         lines = f.read().splitlines()[10:]
         for line in lines:
            fdata = line.split('|')
            
            # Apply the tests from the arguments, storing each in a separate boolean
            cik_inc = fdata[0] == cik or cik is None
            company_inc = company is None or fdata[1].lower() == company.lower()
            form_inc = forms is None or fdata[2] in forms
            try:
               sic_inc = sicIndex[fdata[0]] == sic or sic is None
            except:
               sic_inc = False # the index might be out of date and missing a company

            if cik_inc and company_inc and form_inc and sic_inc:
               # if there is a keyphrase search, do that now
               if keyphrases is not None:
                  try:
                     doc = urllib2.urlopen('ftp://ftp.sec.gov/' + fdata[4])
                     flag = False
                     for phrase in keyphrases:
                        if phrase.lower() in doc.read().lower():
                           flag = True
                     if not flag:
                        continue
                  except:
                     continue
                     # do nothing and just keep going; some files are just missing.
               results.append({'cik': fdata[0], 'company': fdata[1], 'form': fdata[2],
                               'date': fdata[3], 'url': 'ftp://ftp.sec.gov/' + fdata[4]})
   return results
