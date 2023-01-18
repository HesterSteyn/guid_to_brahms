from os import path
import pandas as pd
from readCSV import readCSV

#this is a new comment

#SCRIPT
filepath = r'C:\NSCF\Ian\GeorefToolToBODATSA' #empty string if local directory
filename = "PRE Senecio Marinda_georeferences2022-11-21T14_53_13.368Z_QDSUpdates_llResUpdates.csv"
fieldname = 'catalogNumber'
file = path.join(filepath,filename)
matchFilename = "SANBI_GUID_Export20221221_121236.csv"
matchFile = path.join(filepath,matchFilename)
df = pd.read_csv(file)
df["Guid"] = None

#read matching csv file and transform to dictionary for fast lookup
matchRecords = readCSV(matchFile)

brahmsIndex = {}

for matchRecord in matchRecords:
    indexKey = matchRecord['SpecimenBarcode']
    identifier = matchRecord["Collection Event Guid"]
    brahmsIndex[indexKey] = identifier


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
