import json
from numpy import *

with open('hdxData.json') as json_data:
    data = json.load(json_data)
    #print(data[0])


 


def node_position(name, type):
    #print (name, type)
    pos = -1    #-1= not found
    for index, item in enumerate(data_nodes):
        if ((item['name'] == name ) and (item['type'] == type)):
            pos = item['id']
            break 
    return pos
    

def compare_tags(a,b):
    if (len(a)>0) and (len(b)>0):
        count = 0
        for i in range(len(a)):
            #print (i, a)
            for j in range(len(b)):
                if (a[i]==b[j]):
                    count+=1
        strength = (count*2)/(len(a)+len(b))
    else:
        strength = 0
    return strength


# def define_dataset_links(nodes):  #links between datasets based on number of matching tags
#     #print ("XXXXXX ", nodes)
#     def dedupe(x):          #remove duplicates (assume duplicated tags are errors)
#         return list(set(x))

#     new_links = []
#     for i in range(len(nodes)):
#         # if i==1000:
#         #     print (nodes[i])
#         for j in range(i + 1, len(nodes)):
#             #print (j)
#             # if j==1000:
#             #     print (j)
#             #print (nodes[i], nodes[j])
#             strength = compare_tags(dedupe(nodes[i]['tags']), dedupe(nodes[j]['tags']))
#             if (strength>=0.8):
#                 #print (strength, nodes[i]['tags'], nodes[j]['tags'])
#                 new_link = {}
#                 new_link['source'] = nodes[i]['id']
#                 new_link['target'] = nodes[j]['id']
#                 new_link['strength'] = strength           #strength=1 correct here?
#                 new_links.append(new_link)
#     return new_links


def define_dataset_links(nodes, diff_orgs_only):  #links between datasets based on number of matching tags but ONLY if not from same org
    #print ("XXXXXX ", nodes)
    def dedupe(x):          #remove duplicates (assume duplicated tags are errors)
        return list(set(x))

    new_links = []
    for i in range(len(nodes)):
        # if i==1000:
        #     print (nodes[i])
        for j in range(i + 1, len(nodes)):
            #print (j)
            # if j==1000:
            #     print (j)
            #print (nodes[i], nodes[j])
            if (nodes[i]['org'] != nodes[j]['org']) or (diff_orgs_only==False):
                strength = compare_tags(dedupe(nodes[i]['tags']), dedupe(nodes[j]['tags']))
                if (strength>=1.0):
                    #print (strength, nodes[i]['tags'], nodes[j]['tags'])
                    new_link = {}
                    new_link['source'] = nodes[i]['id']
                    new_link['target'] = nodes[j]['id']
                    new_link['strength'] = strength           #strength=1 correct here?
                    new_links.append(new_link)
    return new_links




data_trans = {} 
data_nodes = []
data_links = []
data_datasets = []
i = 0
num_orgs = 0
num_datasets = 0

for dataset in data:  #classify orgs and titles (i.e. datasets) as nodes and draw a link for each data entry
    for cat in dataset:        
        if cat=="org":  
            node = {}
            node['name'] = dataset[cat]
            node['type'] = 'org'
            node['id'] = i
            #print (node)
            #data_nodes.append(node)
            node_pos = node_position(node['name'], node['type'])
            if node_pos == -1:          #node doesn't already exists   #note: org names must be unique
                data_nodes.append(node)
                #print(node)
                id_source = node['id']
                i += 1
                num_orgs += 1
            else:                       #node already exists
                id_source = node_pos

        elif cat=="title":
            node = {}
            node['name'] = dataset[cat]
            node['type'] = 'data'
            node['id'] = i     
            node['tags'] = dataset['tags'] 
            node['org'] = dataset['org']

        # node_pos = node_position(node['name'], node['type'])
        # if node_pos == -1:          #node doesn't already exist  
        #create new node for every dataset (even if it shares name with another - allowed to have same name)
            data_nodes.append(node)
            id_target = node['id']
            data_datasets.append(node)
            i += 1
            num_datasets += 1
        # else:                       #node already exists
        #     id_target = node_pos

    
    #print (num_datasets)             
    
    link = {}
    link['source'] = id_source
    link['target'] = id_target
    link['strength'] = -1            #strength=-1 implies link between dataset & org
    data_links.append(link)

    # if (num_datasets >= 415) and (num_datasets <= 418):
    #     print ("Num_datasets: ", num_datasets)
    #     print ("Links so far: ", str(len(data_links)));
    #     print (link)
    #     print (dataset)
    #     print ('******************************************')



# print ("Number of nodes: ", str(len(data_trans['nodes'])));
# print ("Number of orgs: ", str(num_orgs));
print ("Number of datasets: ", str(num_datasets));
# print ("Number of links: ", str(len(data_trans['links'])));

print ("Number of datasets: ", str(len(data_datasets)));
diff_orgs_only = True
new_dataset_links = define_dataset_links(data_datasets, diff_orgs_only)
#new_dataset_links = define_dataset_links_diff_orgs_only(data_datasets)  
print ("Number of new_dataset_links: ", str(len(new_dataset_links)))
#print ("new_dataset_links: ", new_dataset_links)
data_links.extend(new_dataset_links)

data_trans['nodes'] = data_nodes
data_trans['links'] = data_links

with open('data/data.json', 'w') as outfile:  
    json.dump(data_trans, outfile)