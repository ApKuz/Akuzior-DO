# This code concatenates the localization and transform DataFrames and 
# creates a scatter mapbox plot of the data. 
# The purpose of this code is to display the data in an interactive map 
# that makes it easy to visualize the data.

from localization import *
from transform import tDF
from pose import pDF


concatDF = pd.concat([lDF, tDF, pDF])

fig = px.scatter_mapbox(concatDF, lat='lat', lon='lon', color='dataType')
fig.update_layout(mapbox_style="open-street-map")
fig.show()