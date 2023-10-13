# This code will take in a json file and parse through it to get the easting and
# northing values. It will then convert these to lattitude and longitude values
# and plot them on a map.
# The data represents a car's path.
# The context in which this code is used is to plot a car's path on a map.

import plotly.express as px
from jsonDF import _df
import pandas as pd
import numpy as np
import utm

    
# drop any rows where the transform column is NaN
tDF = _df.dropna(subset=['transforms'])

# Creating two new columns for lattitude and longitude
tDF['lat'] = ''
tDF['lon'] = ''

# narrowing the dataframe to only the below columns
flags = ['timeField', 'transforms', 'lat', 'lon']
tDF = tDF[flags]

# reseting the indicies as cutting out rows leaves gaps in the index
tDF = tDF.reset_index()


errorList = []
for index, row in tDF.iterrows():
    
    # extract easting and northing from transforms field
    easting = tDF['transforms'][index][0]['transform']['translation']['x']
    northing = tDF['transforms'][index][0]['transform']['translation']['y']
    
    # easting must follow the below parameters
    if not (easting >= 100_000 and easting <= 1_000_000):
        errorList.append((easting, northing))
        continue
    
    # finding the latlong with provided UTM
    latLong = utm.to_latlon(easting, northing, 17, 'N')
    
    # setting the lat and lon values in df
    tDF.at[index, 'lat'] = latLong[0]
    tDF.at[index, 'lon'] = latLong[1]
    tDF.at[index, 'dataType'] = 'transforms'
    
    
# dropping na values from lat and lon (if any)    
tDF['lat'].replace('', np.nan, inplace=True)

tDF = tDF.dropna(subset=['lat'])
tDF = tDF.dropna(subset=['lon'])

# value checking  
# for index, row in df.iterrows():
#     print(f'{index}, {df["lat"][index]}')
    
if __name__ == '__main__':
    fig = px.scatter_mapbox(tDF, lat='lat', lon='lon', color='brake')
    fig.update_layout(mapbox_style="open-street-map")
    fig.show()