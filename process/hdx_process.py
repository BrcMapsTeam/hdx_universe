import json
from random import shuffle

with open('hdxDataScrape.json') as json_data:
    data = json.load(json_data)

links = []
linkdict = {}
id1 = 0
for item in data:
    linkdict['n'+str(id1)] = [];
    print id1
    id2 = 0
    for item2 in data:
        if(id2>id1):
            overlap = len([val for val in item['t'] if val in item2['t']])
            possible = float(max(len(item['t']),len(item2['t'])))
            value = (overlap/possible)*10
            if overlap>1:
                link = {'s':id1,'t':id2,'v':value}
                linkdict['n'+str(id1)].append(link)

        id2=id2+1
    id1=id1+1

for key in linkdict:
    print key
    shuffle(linkdict[key])
    linkdict[key].sort(key=lambda x: x['v'], reverse=True)
    length = len(linkdict[key])
    if length>0:
        links.append(linkdict[key][0])
    if length>1:
        links.append(linkdict[key][1])
    #if length>2:
    #    links.append(linkdict[key][2])        

with open('hdxDataLinks2.json', 'w') as file:
    json.dump(links, file)

