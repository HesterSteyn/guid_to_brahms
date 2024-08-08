from os import path
import pandas as pd
import csv

#SCRIPT
filepath = r'C:\NSCF\Ian\GeorefToolToBODATSA' #empty string if local directory
filename = "SANBI Vernonia 2023_georeferences_QDS_llResUpdates.csv"
fieldname = 'catalogNumber'
file = path.join(filepath,filename)
matchFilename = "SANBI_GUID_Export20221221_121236.csv"
matchFile = path.join(filepath,matchFilename)
df = pd.read_csv(file)
df["Guid"] = None

#read matching csv file and transform to dictionary for fast lookup

brahmsIndex = {}

try:
    with open(matchFile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            indexKey = row['SpecimenBarcode']
            identifier = row["Collection Event Guid"]
            brahmsIndex[indexKey] = identifier
except:
    print("file or fieldname invalid")

# iterate through  georeferenced records and update GUID based on matched barcode
for index, row in df.iterrows(): 
    barcode = row.loc[fieldname]
    
    if barcode:
        try:
            if barcode in brahmsIndex.keys():
                guid = brahmsIndex[barcode]
                df.loc[index, "Guid"] = guid
        except:
            i = 0 #do nothing


newfilename = filename.replace('.csv', '_GuidUpdates.csv')
df.to_csv(path.join(filepath, newfilename), index = False)
