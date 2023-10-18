import pandas as pd

# Opening the driveOhio provided json file
# To make this work on your machine change the file pathing inside of the open call
with open('../blueroute1export.json') as f:
    _df = pd.read_json(f)