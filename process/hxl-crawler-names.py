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
cutTags = ['geodata','hxl','polygon','geodatabase','shapefile']
for i in range(0, loops):
	result = find_datasets(1000*i, 1000)
	packages = result["results"]
	for package in packages:
		item = {}
		item['i'] = package['id']
		item['n'] = package['title']
		item['d'] = package['total_res_downloads']
		item['t'] = []
		item['h'] = 0
		for tag in package['tags']:
			if tag['name'].lower() not in cutTags:
				item['t'].append(tag['name'].lower())
			if tag['name'].lower() == 'hxl':
				item['h'] = 1
		countries =  json.loads(package['solr_additions'])
		for tag in countries['countries']:
			item['t'].append(tag)
		item['o'] = package['organization']['title']
		output.append(item)

with open('hdxDataScrape.json', 'w') as file:
    json.dump(output, file)