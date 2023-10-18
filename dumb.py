import pandas as pd
import numpy as np
import utm
import time
from location.jsonDF import _df
import plotly.express as px


startTime = time.time()

df = _df
del(_df)

df['lat'] = df['lon'] = df['time'] = np.nan

for index, row in df.iterrows():
   
    try:
        easting = df['transforms'][index][0]['transform']['translation']['x']
        northing = df['transforms'][index][0]['transform']['translation']['y']
        
    except TypeError:
        # setting the lat and lon values in df
        df.at[index, 'lat'] = latLong[0]
        df.at[index, 'lon'] = latLong[1]
        
    else:
        # easting must follow the below parameters
        if not (easting >= 100_000 and easting <= 1_000_000):
            continue
        
        # finding the latlong with provided UTM
        latLong = utm.to_latlon(easting, northing, 17, 'N')
        
        # setting the lat and lon values in df
        df.at[index, 'lat'] = latLong[0]
        df.at[index, 'lon'] = latLong[1]
        
    df.at[index, 'time'] = df['timeField'][index]['$date']
    
df = df.dropna(subset = ['drivingMode'])

fig = px.scatter_mapbox(df, lat='lat', lon='lon', color='drivingMode', hover_data=['time'])
fig.update_layout(mapbox_style="open-street-map")
fig.show()
    

print(f'{round(time.time() - startTime, 3)} seconds')
        