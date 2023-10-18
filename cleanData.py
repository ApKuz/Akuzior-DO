# This code is used to convert the easting and northings from the driveOhio provided json file to lat and long
# it relies on the the field given to the function as a string
# this code also drops any rows that do not have a lat or long value
# the lat and long values are then plotted on a map

import plotly.express as px
from jsonDF import _df
import pandas as pd
import numpy as np
import utm

def cleanData(field):
        
    # drop any rows where the field column is NaN
    newDF = _df.dropna(subset=[field])

    # narrowing 
    flags = ['timeField', field, 'lat', 'lon', 'dataType']
    newDF = newDF.reindex(columns=flags)

    # resseting the indicies as cutting out rows leaves gaps in the index
    newDF = newDF.reset_index()


    errorList = []

    # iterating through each row of the new dataframe to enter lat and lon coordinates
    for index, row in newDF.iterrows():
        
        if field == 'transforms':
            # extract easting and northing from transforms field
            easting = newDF[field][index][0]['transform']['translation']['x']
            northing = newDF[field][index][0]['transform']['translation']['y']
        else:
            # extracting easting and northing from localization or pose field
            easting = newDF[field][index]['position']['x']
            northing = newDF[field][index]['position']['y']
        
        # easting must follow the below parameters
        if not (easting >= 100_000 and easting <= 1_000_000):
            errorList.append((easting, northing))
            continue
        
        # finding the latlong with provided UTM
        latLong = utm.to_latlon(easting, northing, 17, 'N')
        
        # setting the lat and lon values in df
        newDF.at[index, 'lat'] = latLong[0]
        newDF.at[index, 'lon'] = latLong[1]
        newDF.at[index, 'dataType'] = field
        
        
    # dropping na values from lat and lon (if any)    
    newDF['lat'].replace('', np.nan, inplace=True)
    newDF = newDF.dropna(subset=['lat'])
    newDF = newDF.dropna(subset=['lon'])
    


    # return new dataframe
    return newDF