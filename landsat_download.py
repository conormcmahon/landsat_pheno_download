import json
from landsatxplore.api import API
from landsatxplore.earthexplorer import EarthExplorer
import argparse
import subprocess

# user input    
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', required=True, help='Username')
parser.add_argument('-p', '--password', required=True, help='Password')
parser.add_argument('-la', '--latitude', required=True, help='Latitude')
parser.add_argument('-lo', '--longitude', required=True, help='Longitude')
parser.add_argument('-ds', '--start', required=True, help='Start Date')
parser.add_argument('-de', '--end', required=True, help='End Date')
parser.add_argument('-d', '--dataset', required=True, help='Dataset')
parser.add_argument('-c', '--cloud', required=True, help='Max Cloud Cover')

args = parser.parse_args()

username = args.username
password = args.password     
latitude = args.latitude
longitude = args.longitude     
start = args.start
end = args.end     
dataset = args.dataset    
cloud_max = args.cloud     

print("\nStarting request to download data from " + dataset + " from " + start + " to " + end)
print("  Data will be spatially limited between " + latitude + " N and " + longitude + " E. No scenes with more than " + cloud_max + " percent cloud cover.")

# Initialize a new API instance and get an access key
api = API(username, password)

# Search for Landsat TM scenes
scenes = api.search(
    dataset=dataset,
    latitude=float(latitude),
    longitude=float(longitude),
    start_date=start,
    end_date=end,
    max_cloud_cover=cloud_max
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
    # The below command uses the native python downloader in LandsatXPlore, but if it throws an error the whole process will break
    #ee.download(scene['entity_id'], output_dir='./data', dataset=dataset)
    # This runs the commandline utility for LandsatXPlore in a subprocess so that if it errors out, more scenes can still be downloaded
    subprocess.run(['landsatxplore', 'download', scene['entity_id'], '-d', dataset, '-u', username, '-p', password])
    # This hackily directly downloads the scene, circumventing problems that LandsatXPlore is having with donwloading Landsat Collection 2 Level 2 imagery (as of Oct. 19 2021)
    #    check this for more info... I attempted these workarounds, without success: https://github.com/yannforget/landsatxplore/issues/42
    #    This will hard-code an attempt to download from the Landsat 8 C2-L2 data product ID 5e83d14fec7cae84. May need to use others for certain dates? 
    #    Took the download code from this: https://stackoverflow.com/questions/22676/how-to-download-a-file-over-http
#    url = " https://earthexplorer.usgs.gov/download/5e83d14fec7cae84/" + scene['entity_id'] + "/EE/"
#    print("Attempting to directly download from " + url)
#    file_name = url.split('/')[-1]
#    u = urllib2.urlopen(url)
#    f = open(file_name, 'wb')
#    meta = u.info()
#    file_size = int(meta.getheaders("Content-Length")[0])
#    #print "Downloading: %s Bytes: %s" % (file_name, file_size)
#
#    file_size_dl = 0
#    block_sz = 8192
#    while True:
#        buffer = u.read(block_sz)
#        if not buffer:
#            break
#
#        file_size_dl += len(buffer)
#        f.write(buffer)
#        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
#        status = status + chr(8)*(len(status)+1)
#        print(status),
#
#    f.close()


ee.logout()
