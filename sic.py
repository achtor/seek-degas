import csv

sicIndex = {}

with open('sic.csv', 'r') as csvf:
   r = csv.reader(csvf)
   for row in r:
      sicIndex[row[1]] = row[2]

