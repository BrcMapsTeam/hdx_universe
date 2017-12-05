import ckanapi, json, sys, time

DELAY = 2
"""Time delay in seconds between datasets, to give HDX a break."""

CKAN_URL = "https://data.humdata.org"
"""Base URL for the CKAN instance."""


# return all datasets
#def get_all_datasets(start, rows):
    #return ckan.action.package_search(start=start, rows=rows, fq="tags:hxl")   #Return hxl datasets
    #return ckan.action.package_search(start=start, rows=rows)           #use package_list instead?
    #return ckan.action.package_list(); #show(id=package_id);

# Open a connection to HDX
ckan = ckanapi.RemoteCKAN(CKAN_URL)
# result_start_pos = 0
# result_page_size = 6000

# result = get_all_datasets(result_start_pos, result_page_size)
# print('result = ' + str(result['count']))
# result_total_count = result["count"]
# print('result count = ' + str(len(result)))

# #print (str(result))
# packages = result["results"]
# print ('Num packages: ' + str(len(packages)))
# #print ('Packages: ' + str(packages))

hdxData = []

i=0
j=0
# Iterate through all the datasets ("packages") and resources on HDX
for package_id in ckan.action.package_list():
    package = ckan.action.package_show(id=package_id)
    if format(package['type'])=='dataset':
        # print (package)
        dataset = {}
        dataset['title'] = format(package['title'])
        # print (dataset['title'])
        dataset['source'] = "{}".format(package['dataset_source']) #format(package["dataset_source"])
        # print (dataset['source'])
        dataset['org'] = "{}".format(package["organization"]["title"])
        # print (dataset['org'])
        dataset['tags'] = []
        for tag in package["tags"]:
            dataset['tags'].append(tag['display_name'])
        # print (dataset['tags'])
        dataset['num_resources'] = format(package["num_resources"])
        # #print (dataset['num_resources'])
        # print (dataset)
        hdxData.append(dataset)
        print (i)
        i+=1

    # print ("")
    # print (str(i) + " - Package: " + format(package["title"]))
    # print ("               " + format(package["dataset_source"]))
    # print ("               " + format(package["organization"]["title"]))
    # print ("               " + format(package["num_tags"]) + ' tags')
    # for tag in package["tags"]:
    #     print ("               " + tag['display_name'])
    # print ("               " + format(package["num_resources"]) + ' resources')
    # print ("---------------------")
    # i+=1

    #for each resource in a package (some packages have multiple csv files for example), print the name, url and format
    #j=0
    #for resource in package["resources"]:  
    #    j+=1
    #     print (j) 
    #     print (str(j) + "  {}".format(resource["name"].encode('ascii', 'ignore')))
    #     print (str(j) + "    {}".format(resource["url"]))
    #     print (str(j) + " " + str(resource["format"]))
    #     time.sleep(DELAY) # give HDX a short rest

#print (hdxData)
#print (j)
print (i)

with open('hdxData_2.json', 'w') as file:
    json.dump(hdxData, file)