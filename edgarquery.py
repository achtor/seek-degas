import urllib2
from datetime import date
def edgar(func):
   def inner(start = 1993, end = int(date.today().year), forms = None, company = None,
               cik = None, sic = None, keyphrases = None, **kwargs):
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
               continue
            lines = f.read().splitlines()[10:]
            for line in lines:
               fdata = line.split('|')
               # Apply the tests from the arguments, storing each in a separate boolean
               cik_inc = fdata[0] == cik or cik is None
               company_inc = company is None or fdata[1].lower() == company.lower()
               form_inc = forms is None or fdata[2] in forms
               try:
                  sic_inc = sic is None or sicIndex[fdata[0]] == sic
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
                  yield func(fdata,**kwargs)
   return inner

@edgar
def query(fdata):
   return {'cik': fdata[0], 'company': fdata[1], 'form': fdata[2],
          'date': fdata[3], 'url': 'ftp://ftp.sec.gov/' + fdata[4]}

@edgar
def download(fdata,regex = None, regopt = None, filepath = '', prefix = ''):
   try: 
      f = urllib2.urlopen('ftp://ftp.sec.gov/' + fdata[4])
   except:
      return
   if regex is not None:
      wtext = re.findall(regex, f.read(), regopt)
      if len(wtext) == 0:
         return
   else:
      wtext = f.read()
      with open(filepath + prefix + fdata[0] + '-' + fdata[3] + '.txt','w'):
         g.write(wtext)

