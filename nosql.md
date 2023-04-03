In implementing the bristol-air-quality data to a NoSQL database, MongoDB and Python were used to carry out this task. MongoDB, a NoSQL document database is defined as ordered sets of key-value pairs synonymous to rows in SQL . Data is stored as documents,  converged as collections and stored in a database. Additionally, MongoDB uses JSON to store and transport data. 

MongoDB schema's flexibility was good for the assignment as the properties of documents in the collection varied. Fields in documents with Null or NAN values in the data, were ignored. 

Highlighted below are the data modelling and implementation steps in sequence: 

# CREATING A MONGODB ACCOUNT/CLUSTER:
The first step was to generate a free MongoDB cloud account. Also, created was a username, password, project, cluster and connection settings needed for the collection.

# DOWNLOADING PACKAGES AND IMPORTING LIBRARIES:
After the account generation, pymongo and dnspython were downloaded through the command prompt(pip install) to enable the seamless connection and querying of database in MongoDB through Python. Also, I  imported the necessary libraries such as Pandas, JSON and urllib.

# DATA MODELLING/INSERTING DOCUMENTS TO THE COLLECTION:
For emphasis, MongoDB is a document database with key-value pairs. Therefore, the data from the 'clean.csv' was modeled with the below schema: 

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
                    "bsonType": "double"
                },
                "NO2": {
                    "bsonType": "double"
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

# READING THE DATA SET AND SELECTING SITE ID 459
This process involves running the below codes in Python and transforming the csv fie to JSON:

data = pd.read_csv('clean.csv', low_memory= False)
indexed_data = data.set_index('SiteID') # For setting the siteID as the index
part_data = indexed_data.loc[459].reset_index(drop=True) # For picking the siteId of 459 
part_data.fillna('Empty', inplace=True) # Replacing null values with the string empty to aid conversion to JSON data.
data_index = part_data.rename(columns={'geo_point_2d': 'GeoPoint2D'}).reset_index() # Renaming Geopoint2D to fit MongoDB structure and ensuring there is an index column

# Creating a column for unique values assigned to each row of the csv to prevent duplication
Although MongoDB generates a primary key, I wanted to prevent duplication of documents. Thus, I created a field called _id as my index:
columns = list(data_index.columns)
columns[0] = '_id' 

# Creating a function to easily convert file to NoSQL JSON type by dropping NAN column values renamed 'Empty':
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

# Writing a function to create database instance and collection name:
def get_database(username, password, cluster_url, dbname):
    username = urllib.parse.quote(username)
    password = urllib.parse.quote(password)
    
    CONNECTION_STRING = f"mongodb+srv://{username}:{password}@{cluster_url}/{dbname}"
    
    # Creating a connection using MongoClient
    client = pymongo.MongoClient(CONNECTION_STRING)
    
    return client[dbname]

# CONNECTING AND TRANSFERRING TO THE MONGODB CLUSTER
Finally, the data is connected to the MongoDB cluster with the collection and database created by:

connect_url = "cluster0.hzlgk.mongodb.net"
assess = get_database('maro', '1991', connect_url, 'dmf')
maro_test = assess.create_collection('site_459_', validator=document_db)

maro_test.insert_many([x for x in values]) #inserting the json document created earlier as a list in the database.

# QUERIES:
print(assess.site_459_.count_documents({}))

value = assess.site_459_.find({"NO": {"$lt": 25}}).limit(5) #rows where NO value is less than 25

for x in value:
    print(x)

# RESULTS:
8761
{'_id': 32, 'Date Time': '2010-06-17 06:00:00+00:00', 'NOx': 75.03, 'NO2': 38.34, 'NO': 23.92, 'Location': 'Cheltenham Road \\ 
Station Road', 'GeoPoint2D': '51.4689385901,-2.5927241667', 'DateStart': '2008-06-25T00:00:00+00:00', 'DateEnd': '2011-12-31T00:00:00+00:00', 'Current': False, 'Instrument Type': 'Continuous (Reference)'}
{'_id': 33, 'Date Time': '2010-06-16 14:00:00+00:00', 'NOx': 66.09, 'NO2': 38.52, 'NO': 17.98, 'Location': 'Cheltenham Road \\ 
Station Road', 'GeoPoint2D': '51.4689385901,-2.5927241667', 'DateStart': '2008-06-25T00:00:00+00:00', 'DateEnd': '2011-12-31T00:00:00+00:00', 'Current': False, 'Instrument Type': 'Continuous (Reference)'}
{'_id': 34, 'Date Time': '2010-06-15 16:00:00+00:00', 'NOx': 58.02, 'NO2': 33.48, 'NO': 16.01, 'Location': 'Cheltenham Road \\ 
Station Road', 'GeoPoint2D': '51.4689385901,-2.5927241667', 'DateStart': '2008-06-25T00:00:00+00:00', 'DateEnd': '2011-12-31T00:00:00+00:00', 'Current': False, 'Instrument Type': 'Continuous (Reference)'}
{'_id': 35, 'Date Time': '2010-06-15 08:00:00+00:00', 'NOx': 67.56, 'NO2': 35.57, 'NO': 20.86, 'Location': 'Cheltenham Road \\ 
Station Road', 'GeoPoint2D': '51.4689385901,-2.5927241667', 'DateStart': '2008-06-25T00:00:00+00:00', 'DateEnd': '2011-12-31T00:00:00+00:00', 'Current': False, 'Instrument Type': 'Continuous (Reference)'}
{'_id': 38, 'Date Time': '2010-06-14 04:00:00+00:00', 'NOx': 15.49, 'NO2': 8.05, 'NO': 4.85, 'Location': 'Cheltenham Road \\ Station Road', 'GeoPoint2D': '51.4689385901,-2.5927241667', 'DateStart': '2008-06-25T00:00:00+00:00', 'DateEnd': '2011-12-31T00:00:00+00:00', 'Current': False, 'Instrument Type': 'Continuous (Reference)'}
