# This code is used to convert the easting and northings from the driveOhio provided json file to lat and long
# it relies on the localization entry
# this code also drops any rows that do not have a lat or long value
# the lat and long values are then plotted on a map

import plotly.express as px
from jsonDF import _df
import pandas as pd
import numpy as np
import utm

    
# drop any rows where the transform column is NaN
lDF = _df.dropna(subset=['localization'])

# Creating two new columns for lattitude and longitude
lDF['lat'] = ''
lDF['lon'] = ''
lDF['dataType'] = ''

# narrowing the dataframe to only the below columns

flags = ['timeField', 'localization', 'lat', 'lon', 'dataType']
lDF = lDF[flags]

# resseting the indicies as cutting out rows leaves gaps in the index
lDF = lDF.reset_index()


errorList = []
for index, row in lDF.iterrows():
    
    # extract easting and northing from transforms field
    easting = lDF['localization'][index]['position']['x']
    northing = lDF['localization'][index]['position']['y']
    
    # easting must follow the below parameters
    if not (easting >= 100_000 and easting <= 1_000_000):
        errorList.append((easting, northing))
        continue
    
    # finding the latlong with provided UTM
    latLong = utm.to_latlon(easting, northing, 17, 'N')
    
    # setting the lat and lon values in df
    lDF.at[index, 'lat'] = latLong[0]
    lDF.at[index, 'lon'] = latLong[1]
    lDF.at[index, 'dataType'] = 'localization'
    
    # print(f'index: {index}\neasting: {easting}\nnorthing: {northing}')
    
    
# dropping na values from lat and lon (if any)    
lDF['lat'].replace('', np.nan, inplace=True)

lDF = lDF.dropna(subset=['lat'])
lDF = lDF.dropna(subset=['lon'])

# value checking  
# for index, row in df.iterrows():
#     print(f'{index}, {df["lat"][index]}')
    
if __name__ == '__main__':
    fig = px.scatter_mapbox(lDF, lat='lat', lon='lon', color='dataType')
    fig.update_layout(mapbox_style="open-street-map")
    fig.show()