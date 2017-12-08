import ckanapi, json
from urllib2 import Request, urlopen, URLError, HTTPError
import math

CKAN_URL = "https://data.humdata.org"
"""Base URL for the CKAN instance."""


def find_datasets(start, rows):
    """Return a page of HXL datasets."""
    return ckan.action.package_search(start=start, rows=rows)

# Open a connection to HDX
ckan = ckanapi.RemoteCKAN(CKAN_URL)


result = find_datasets(0, 0)
result_total_count = result["count"]
numOfFiles =  result["count"]
#loops = int(math.ceil(numOfFiles/1000))
output = []
loops = 7
j=0
item = {}
cutTags = ['geodata','hxl','polygon','geodatabase','shapefile']
for i in range(0, loops):
	result = find_datasets(1000*i, 1000)
	packages = result["results"]
	for package in packages:
		print j
		item['notes'] = package['notes']
		filepath = 'description/'+package['id']+'.json'
		with open(filepath, 'w') as file:
		    json.dump(item, file)
		j=j+1