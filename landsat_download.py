import json
from landsatxplore.api import API
from landsatxplore.earthexplorer import EarthExplorer
import argparse

# user input    
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', required=True, help='Username')
parser.add_argument('-p', '--password', required=True, help='Password')
parser.add_argument('-la', '--latitude', required=True, help='Latitude')
parser.add_argument('-lo', '--longitude', required=True, help='Longitude')
parser.add_argument('-ds', '--start', required=True, help='Start Date')
parser.add_argument('-de', '--end', required=True, help='End Date')
parser.add_argument('-d', '--dataset', required=True, help='Dataset')

args = parser.parse_args()

username = args.username
password = args.password     
latitude = args.latitude
longitude = args.longitude     
start = args.start
end = args.end     
dataset = args.dataset     

print("\nStarting request to download data from " + dataset + " from " + start + " to " + end)
print("  Data will be spatially limited between " + latitude + " N and " + longitude + " E.")

# Initialize a new API instance and get an access key
api = API(username, password)

# Search for Landsat TM scenes
scenes = api.search(
    dataset=dataset,
    latitude=float(latitude),
    longitude=float(longitude),
    start_date=start,
    end_date=end,
    max_cloud_cover=10
)

print(f"{len(scenes)} scenes found.")

# List Scenes
for scene in scenes:
    print("Found a scene from " + scene['acquisition_date'].strftime('%Y-%m-%d'))

api.logout()

# Download Scenes
ee = EarthExplorer(username, password)
for scene in scenes:
    print("Downloading a scene from " + scene['acquisition_date'].strftime('%Y-%m-%d') + " with ID " + scene['entity_id'])
    ee.download(scene['entity_id'], output_dir='./data', dataset=dataset)

ee.logout()
