# This code creates new dataframes based on the field input to the cleandata() function
# creates a scatter mapbox plot of the data. 
# The purpose of this code is to display the data in an interactive map 
# that makes it easy to visualize the data.

import pandas as pd
import plotly.express as px
from cleanData import cleanData

# creating dataframs from these fields
lDF = cleanData('localization')
tDF = cleanData('transforms')
pDF = cleanData('pose')

# concatenating all dataframes into a singular one
concatDF = pd.concat([lDF, tDF, pDF])

# creating plot and opening it in browser
fig = px.scatter_mapbox(concatDF, lat='lat', lon='lon', color='currentVehicle', mapbox_style="open-street-map")
fig.show()