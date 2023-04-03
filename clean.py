import pandas as pd
try: 
    #low_memory=False parameter added to override low memory error message
    data = pd.read_csv('crop.csv', low_memory=False)

    # site_ids(keys) and locations(values) written as a dictionary
    site_ids = { 
        188: "AURN Bristol Centre",
        203: "Brislington Depot",
        206: "Rupert Street",
        209: "IKEA M32",
        213: "Old Market",
        215: "Parson Street School",
        228: "Temple Meads Station",
        270: "Wells Road",
        271: "Trailer Portway P&R",
        375: "Newfoundland Road Police Station",
        395: "Shiner's Garage",
        452: "AURN St Pauls",
        447: "Bath Road",
        459: "Cheltenham Road \ Station Road",
        463: "Fishponds Road",
        481: "CREATE Centre Roof",
        500: "Temple Way",
        501: "Colston Avenue",
    }

    #Getting the location of the site with .get dictionary method
    def get_location(ids):
        loc= site_ids.get(ids, False)

    #If the site ID is not in the dictionary, it returns false
        if loc is False:
            return False
        else: #returns the location
            return loc

    #Selecting and printing null or mismatched values
    null_or_mismatched= data[(data['SiteID'].apply(get_location)==data['Location'])==False]
    print(null_or_mismatched)

    #Printing matched values
    newdata = data[(data['SiteID'].apply(get_location)==data['Location'])==True]
    print(newdata)

    #creating cleaned csv file
    newdata.to_csv('clean.csv', index= False)
except:
    print('error')