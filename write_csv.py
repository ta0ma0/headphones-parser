import json
import csv

line = open('headphones.csv').read().replace("'", '"')
table = json.loads(line)

# print(table[0])
myFile = open('head_csv.csv', 'w')
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(table)