from pymongo import MongoClient

client = MongoClient()
db = client.animalclothes
collection = db.animals

docs = collection.aggregate([{'$group': {'_id': '','total_boy_count': { '$sum': '$total_boy_count' }}},{'$project': {'_id': 0,'total_boy_count': '$total_boy_count'}}])
list_of_dicts = []
for doc in docs:
    list_of_dicts.append(doc)
print('Total number of boys clothes = {}'.format(list_of_dicts[0]['total_boy_count']))
total_boy_clothes = list_of_dicts[0]['total_boy_count']

docs = collection.aggregate([{'$group': {'_id': '','total_girl_count': { '$sum': '$total_girl_count' }}},{'$project': {'_id': 0,'total_girl_count': '$total_girl_count'}}])
list_of_dicts = []
for doc in docs:
    list_of_dicts.append(doc)
print('Total number of girls clothes = {}'.format(list_of_dicts[0]['total_girl_count']))
total_girl_clothes = list_of_dicts[0]['total_girl_count']

docs = collection.aggregate([{'$project':{'names':1,'total_boy_count':1,'_id':0}},{'$sort':{'total_boy_count':-1}}])
list_of_dicts = []
for doc in docs:
    list_of_dicts.append(doc)
print('The top 5 animals for boys were...')
count = 0
for item in list_of_dicts:
    if count <= 4:
        print('{} : {} ({:.2f} %)'.format(item['names'][0],item['total_boy_count'],100*(item['total_boy_count']/total_boy_clothes)))
        count += 1

docs = collection.aggregate([{'$project':{'names':1,'total_girl_count':1,'_id':0}},{'$sort':{'total_girl_count':-1}}])
list_of_dicts = []
for doc in docs:
    list_of_dicts.append(doc)
print('The top 5 animals for girls were...')
count = 0
for item in list_of_dicts:
    if count <= 4:
        print('{} : {} ({:.2f} %)'.format(item['names'][0],item['total_girl_count'],100*(item['total_girl_count']/total_girl_clothes)))
        count += 1

docs = collection.aggregate([{ '$project' : { 'names': 1, 'total': { '$add': [ "$total_boy_count", "$total_girl_count" ] } }},{'$sort': {'total':-1 } } ] )
list_of_dicts = []
for doc in docs:
    list_of_dicts.append(doc)
print('The top 5 animals overall were:')
count = 0
for item in list_of_dicts:
    if count <= 4:
        print('{} : {}'.format(item['names'][0],item['total']))
        count += 1

docs = collection.aggregate([{'$project':{'names':1,'total_boy_count':1,'_id':0}},{'$sort':{'total_boy_count':-1}}])
list_of_dicts = []
for doc in docs:
    list_of_dicts.append(doc)
print('All results for boys sorted by number were:')
count = 1
for item in list_of_dicts:
    print('#{}. {} : {} ({:.2f} %)'.format(count,item['names'][0],item['total_boy_count'],100*(item['total_boy_count']/total_boy_clothes)))
    count += 1

docs = collection.aggregate([{'$project':{'names':1,'total_girl_count':1,'_id':0}},{'$sort':{'total_girl_count':-1}}])
list_of_dicts = []
for doc in docs:
    list_of_dicts.append(doc)
print('All results for girls sorted by number were:')
count = 1
for item in list_of_dicts:
    print('#{}. {} : {} ({:.2f} %)'.format(count,item['names'][0],item['total_girl_count'],100*(item['total_girl_count']/total_girl_clothes)))
    count += 1
