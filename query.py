import pandas as pd
import json
import pymongo 
import urllib 

data = pd.read_csv('clean.csv', low_memory= False) # Setting the siteID as the index
indexed_data = data.set_index('SiteID')

part_data = indexed_data.loc[459].reset_index(drop=True) # Picking the siteId of 459

part_data.fillna('Empty', inplace=True) # Replacing null values with the string empty
# This would aid in the conversion to json data

data_index = part_data.rename(columns={'geo_point_2d': 'GeoPoint2D'}).reset_index() # This line ensures there is an index column

columns = list(data_index.columns)
columns[0] = '_id' # creating a column for unique values

values = []
for row in data_index.values:
    dicts = {}
    for ind, val in enumerate(row):
        col = columns[ind]
        if val == "Empty":
            pass
        else:
            dicts[col] = val
    values.append(dicts)

# Saving the file to no-sql format offline 
with open('site_459.json', 'w') as file:
    file.write(json.dumps(values))

def get_database(username, password, cluster_url, dbname):
    username = urllib.parse.quote(username)
    password = urllib.parse.quote(password)
    
    CONNECTION_STRING = f"mongodb+srv://{username}:{password}@{cluster_url}/{dbname}"
    
    # Creating a connection using MongoClient
    client = pymongo.MongoClient(CONNECTION_STRING)
    
    return client[dbname]

# This enforces schema on the document 
document_db = {
        "$jsonSchema":{
            'additionalProperties': True,
            "bsonType": "object",
            "required": [
                "_id",
                "Date Time",
                "Location",
                "GeoPoint2D",
                "DateStart",
                "DateEnd",
                "Current",
                "Instrument Type"
                 
            ],
            "properties": {
                "_id": {
                    "bsonType": "int"
                },
                "Date Time": {
                    "bsonType": "string"
                },
                "Location": {
                    "bsonType": "string",
                    "enum": [
                        "Cheltenham Road \\ Station Road"
                    ],
                    "title": "Location"
                        },
                "GeoPoint2D" : {
                   "bsonType": "string",
                    "enum": [
                        "51.4689385901,-2.5927241667"
                    ],
                    "title": "GeoPoint2D"
                },
                "DateStart": {
                    "bsonType": "string"
                },
                "DateEnd": {
                    "bsonType": "string"
                },
                "Current": {
                    "bsonType": "bool"
                },
                "Instrument Type": {
                    "bsonType": "string"
                },
                "NOx": {
                    "bsonType": "number"
                },
                "NO2": {
                    "bsonType": "number"
                },
                "NO": {
                    "bsonType": "double"
                },
                "PM10": {
                    "bsonType": "double"
                },
                "NVPM10": {
                    "bsonType": "double"
                },
                "VPM10": {
                    "bsonType": "double"
                },
                "NVPM2.5": {
                    "bsonType": "double"
                },
                "PM2.5": {
                    "bsonType": "double"
                },
                "VPM2.5": {
                    "bsonType": "double"
                },
                "CO": {
                    "bsonType": "double"
                },
                "O3": {
                    "bsonType": "double"
                },
                "SO2": {
                    "bsonType": "double"
                },
                "Temperature": {
                    "bsonType": "double"
                },
                "RH": {
                    "bsonType": "double"
                },
                "Air Pressure": {
                    "bsonType": "double"
                }
            }
            
        }
    }

connect_url = "cluster0.hzlgk.mongodb.net"
assess = get_database('maro', '1991', connect_url, 'dmf')
#maro_test = assess.create_collection('site_459_', validator=document_db)
#maro_test.insert_many([x for x in values])

# QUERIES
print(assess.site_459_.count_documents({}))

value = assess.site_459_.find({"NO": {"$lt": 25}}).limit(5) #rows where NO value is less than 25

for x in value:
    print(x)

json_string = json.dumps(value)
print(json_string)

with open('x.json', 'w') as i:
    json.dump(json_string, i)
