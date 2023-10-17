# This code is used to convert the easting and northings from the driveOhio provided json file to lat and long
# it relies on the localization entry
# this code also drops any rows that do not have a lat or long value
# the lat and long values are then plotted on a map

import plotly.express as px
import pandas as pd
from jsonDF import _df
import numpy as np
import utm

    
# drop any rows where the transform column is NaN
pDF = _df.dropna(subset=['pose'])


# narrowing the dataframe to only the below columns
flags = ['timeField', 'pose', 'lat', 'lon', 'dataType']
pDF = pDF.reindex(columns=flags)

# resseting the indicies as cutting out rows leaves gaps in the index
pDF = pDF.reset_index()


errorList = []
for index, row in pDF.iterrows():
    
    # extract easting and northing from transforms field
    easting = pDF['pose'][index]['position']['x']
    northing = pDF['pose'][index]['position']['y']
    
    # easting must follow the below parameters
    if not (easting >= 100_000 and easting <= 1_000_000):
        errorList.append((easting, northing))
        continue
    
    # finding the latlong with provided UTM
    latLong = utm.to_latlon(easting, northing, 17, 'N')
    
    # setting the lat and lon values in df
    pDF.at[index, 'lat'] = latLong[0]
    pDF.at[index, 'lon'] = latLong[1]
    pDF.at[index, 'dataType'] = 'pose'
    
    # print(f'index: {index}\neasting: {easting}\nnorthing: {northing}')
    
    
# dropping na values from lat and lon (if any)    
pDF['lat'].replace('', np.nan, inplace=True)

pDF = pDF.dropna(subset=['lat'])
pDF = pDF.dropna(subset=['lon'])

# value checking  
# for index, row in df.iterrows():
#     print(f'{index}, {df["lat"][index]}')
    
if __name__ == '__main__':
    fig = px.scatter_mapbox(pDF, lat='lat', lon='lon', color='dataType')
    fig.update_layout(mapbox_style="open-street-map")
    fig.show()