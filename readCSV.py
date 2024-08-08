import csv

def readCSV(fileName):
  try:
    records = []
    with open(fileName, newline='', ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            records.append(row)
            rowcount = rowcount + 1
  except Exception as ex:
    print("file or fieldname invalid")

  return records