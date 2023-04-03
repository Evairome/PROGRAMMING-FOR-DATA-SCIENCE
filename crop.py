#import pandas library to read and parse csv
import pandas as pd

try:
    # delimiter (;) indicates that text strings in csv file are seperated by semi-colons
    data_frame = pd.read_csv('bristol-air-quality-data.csv', delimiter=';') 
    print(data_frame)

    #Date Time column is used to select data range
    #Date Time structure changed from string to object which enables use of pandas' date time function
    data_frame['Date Time']=pd.to_datetime(data_frame['Date Time'])
    timestamp =pd.to_datetime('1/1/2010 00:00:00+00:00')

    #.loc method is used to select data range based on required timeframe 
    data_frame2= data_frame.loc[data_frame['Date Time'] >= timestamp]
    print(data_frame2)

    #creating new csv with cropped data
    data_frame2.to_csv('crop.csv', index= False)
except:
    print('error')