import mariadb
import pandas as pd


###################################################################################
#####  CREATE TABLE STATEMENT FOR THE THREE TABLES #####
##### 1. SCHEMA_SQL TABLE #####
##### 2. SITE TABLE #####
##### 3. READING TABLE #####
###################################################################################


# Create table statement for the Schema Table
schema_table = """
CREATE TABLE schema_sql(
    MEASURE VARCHAR(100) NOT NULL,
    DESCRIPTION VARCHAR(150) NOT NULL,
    UNIT VARCHAR(40) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL
    );
"""

# Create table statement for the site_info table
site_table = """
CREATE TABLE site(
    SITEID MEDIUMINT(45) NOT NULL,
    LOCATION VARCHAR(50) DEFAULT NULL,
    GEO_POINT_2D VARCHAR(60) DEFAULT NULL,
    PRIMARY KEY (SiteID));
"""
# table for the readings
reading_table = """
CREATE TABLE IF NOT EXISTS reading (
    READING_ID INT NOT NULL AUTO_INCREMENT, 
    DATE_TIME DATETIME DEFAULT NULL,
    NOX FLOAT DEFAULT NULL,
    NO2 FLOAT DEFAULT NULL,
    NO FLOAT DEFAULT NULL,
    SITEID MEDIUMINT(45) DEFAULT NULL,
    PM10 FLOAT DEFAULT NULL,
    NVPM10 FLOAT DEFAULT NULL,
    VPM10 FLOAT DEFAULT NULL,
    `NVPM2.5` FLOAT DEFAULT NULL,
    `PM2.5` FLOAT DEFAULT NULL,
    `VPM2.5` FLOAT DEFAULT NULL,
    CO FLOAT DEFAULT NULL,
    O3 FLOAT DEFAULT NULL,
    SO2 FLOAT DEFAULT NULL,
    TEMPERATURE FLOAT DEFAULT NULL,
    RH FLOAT DEFAULT NULL,
    `AIR_PRESSURE` FLOAT DEFAULT NULL,
    DATESTART DATETIME DEFAULT NULL,
    DATEEND DATETIME DEFAULT NULL,
    CURRENT TINYINT DEFAULT NULL,
    `INSTRUMENT TYPE` VARCHAR(100) DEFAULT NULL,
    PRIMARY KEY(READING_ID),
    CONSTRAINT fk_type
    FOREIGN KEY (SiteID)
        REFERENCES site(SiteID));
    """

# Reading the clean.csv file
data = pd.read_csv("clean.csv", low_memory= False)


# Creating a function for inserting values
def insert_values(dataframe, table, cols=None):
    # getting values from the dataframe
    values = dataframe.values
    values = tuple((tuple(row) for row in values))

    # Replicating the SQL INSERT INTO statement to insert values
    clean_insert = str(values).strip("(").strip(")")
    if cols is None:
        insert_query = f"INSERT INTO {table} VALUES ({clean_insert});".replace("nan", "NULL")
    else:
        cols = str(cols).replace('"', "`").replace("'", "`")
        insert_query = f"INSERT INTO {table} {cols} VALUES ({clean_insert});".replace("nan", "NULL")

    return insert_query


# The columns for creating the site table
site_values = data[["SiteID", "Location", "geo_point_2d"]].drop_duplicates()
site_table_values = insert_values(site_values, "site")

# Getting the date columns
date_cols = [col for col in data.keys() if "Date" in col]
# Converting the Date Time object to string, to ensure compartibility with SQL
data[date_cols] = data[date_cols].apply(
    lambda date: pd.to_datetime(date).dt.strftime("%Y-%m-%d %H:%M")
)

# Values for the schema table
schema_table_values = (
    ("Date Time", "Date and time of measurement", "datetime"),
    ("NOx", "Concentration of oxides of nitrogen", "㎍/m3"),
    ("NO2", "Concentration of nitrogen dioxide", "㎍/m3"),
    ("NO", "Concentration of nitric oxide", "㎍/m3"),
    ("SiteID", "Site ID for the station", "integer"),
    ("PM10", "Concentration of particulate matter <10 micron diameter", "㎍/m3"),
    ("NVPM10", "Concentration of non - volatile particulate matter <10 micron diameter", "㎍/m3"),
    ("VPM10",  "Concentration of volatile particulate matter <10 micron diameter",  "㎍/m3"),
    ("NVPM2.5","Concentration of non volatile particulate matter <2.5 micron diameter", "㎍/m3"),
    ("PM2.5", "Concentration of particulate matter <2.5 micron diameter", "㎍/m3"),
    ("VPM2.5", "Concentration of volatile particulate matter <2.5 micron diameter", "㎍/m3"),
    ("CO", "Concentration of carbon monoxide", "㎍/m3"),
    ("O3", "Concentration of ozone", "㎍/m3"),
    ("SO2", "Concentration of sulphur dioxide", "㎍/m3"),
    ("Temperature", "Air temperature", "°C"),
    ("RH", "Relative Humidity", "%"),
    ("Air Pressure", "Air Pressure", "mbar"),
    ("Location", "Text description of location", "text"),
    ("geo_point_2d", "Latitude and longitude", "geo point"),
    ("DateStart", "The date monitoring started", "datetime"),
    ("DateEnd", "The date monitoring ended", "datetime"),
    ("Current", "Is the monitor currently operating", "text"),
    ("Instrument Type", "Classification of the instrument", "text"),
)

schema_table_values = str(schema_table_values).strip("(").strip(")")
schema_table_value = f"INSERT INTO schema_sql VALUES ({schema_table_values});"

reading_cols = (
    "DATE_TIME",
    "NOX", "NO2",
    "NO", "SITEID",
    "PM10", "NVPM10",
    "VPM10", "NVPM2.5",
    "PM2.5", "VPM2.5",
    "CO", "O3",
    "SO2", "TEMPERATURE",
    "RH", "AIR_PRESSURE",
    "DATESTART", "DATEEND",
    "CURRENT",  "INSTRUMENT TYPE",)

# Reading table data 
reading_data = data.drop(columns=["Location", "geo_point_2d"])

###################################################################################
#####    THE READING TABLE WAS PARTITIONED INTO 5,000 ROWS #####
##### BECAUSE IT WAS THE MAXIMUM QUERY LIMIT MARIADB COULD HANDLE AT A TIME #####
###################################################################################

# Breaking the reading table into partitions of 5,000 rows
indexes = range(0, len(reading_data), 5000)
num_parts = len(indexes)  # Number of partitions

# Creating a dictionary to hold the various parts of the reading table
reading_values_dict = {}

# Assigning each part to a dictionary
for ind in range(num_parts):
    start = indexes[ind]
    if ind != num_parts - 1:
        stop = indexes[ind + 1]
        reading_values_dict[ind] = insert_values(reading_data[start:stop], "reading", cols=reading_cols)
    else:
        reading_values_dict[ind] = insert_values(reading_data[start:], "reading", cols=reading_cols)

# Instantiate Connection for creating the database
try:
    with mariadb.connect(host="localhost", port=3306, user="root", password="") as connect:

        # Creating the cursor object to execute queries
        cursor = connect.cursor()

        # Executing the queries
        # Dropping an existing pollution-db2
        cursor.execute("DROP DATABASE IF EXISTS `pollution-db2`;")
        cursor.execute("CREATE DATABASE `pollution-db2`;")  # creating the database

        # Ensuring it selects the pollution_db2 database
        cursor.execute("USE `pollution-db2`;")

        # Creating the schema, site and reading tables
        cursor.execute(schema_table)
        cursor.execute(site_table)
        cursor.execute(reading_table)

        # Inserting data into the schema table
        cursor.execute(schema_table_value)

        # Inserting data into the site table
        cursor.execute(site_table_values)

        # inserting the paritions of the reading data into the reading table
        for part in reading_values_dict.values():
            cursor.execute(part)

        # Committing the changes back to the database
        connect.commit()
except mariadb.Error as error:
    print(f"Error connecting to the database: {error}")