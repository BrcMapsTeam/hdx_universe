"""Sample script to crawl HDX.
CKAN API documentation: http://docs.ckan.org/en/latest/api/
Python CKAN library: https://github.com/ckan/ckanapi
Started by David Megginson, 2016-08-25
"""

import ckanapi, time

DELAY = 2
"""Time delay in seconds between datasets, to give HDX a break."""

CKAN_URL = 'https://data.humdata.org'
"""Base URL for the CKAN instance."""

# Open a connection to HDX
ckan = ckanapi.RemoteCKAN(CKAN_URL)

i=0
j=0
# Iterate through all the datasets ("packages") and resources on HDX
for package_id in ckan.action.package_list():
    #package = ckan.action.package_show(id=package_id)
    #print("Package: {}".format(package['title']))
    #for resource in package['resources']:
    #    j += 1
    #    print(j)
        #print("  Resource: {}".format(resource['name']))
        #print("    URL: {}".format(resource['url']))
    #print("")
    if i<3:
        package = ckan.action.package_show(id=package_id)
        print("Package: {}".format(package['title']))
        print("Package: {}".format(package['organization']['title']))
        print (package_id)
    i += 1
    #print (i)
    #time.sleep(DELAY) # give HDX a short rest

print (i,j)
# end