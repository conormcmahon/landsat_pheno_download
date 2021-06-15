# landsat_pheno_download

Downloading dense Landsat timeseries based on [https://github.com/yannforget/landsatxplore](https://github.com/yannforget/landsatxplore).

Search for and download a Landsat timeseries for a given location.

Usage: 

```

python ./landsat_download.py --username USGS_USERNAME --password USGS_PASSWORD --latitude 12.345 --longitude -54.321 --start "2001-01-01" --end "2010-01-01" --dataset landsat_ot_c2_12

```

This will download all Landsat scenes which CONTAIN the lat/lon point selected, between the start and end dates (which are in YYYY-MM-DD). 

For the dataset options, see [https://github.com/yannforget/landsatxplore](https://github.com/yannforget/landsatxplore). Choose a landsat mission (e.g. 5, 8) and product (e.g. Surface Reflectance). 

Currently, this will download all scenes as .tar.gz archives to the ./data/ subdirectory of this repository. 

Most of the code used here is from the examples provided by the base library above. 
