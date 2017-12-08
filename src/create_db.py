from pymongo import MongoClient
client = MongoClient()
db = client.animalclothes
result = db.animals.delete_many({})

list_of_dicts = []

temp_dict = {}
temp_dict['names']=['dinosaur','dinosaurs','dino','dinos','t-rex','t rex','tyrannosaurus rex']
temp_dict['food'] = 'carnivore'
temp_dict['weight'] = 8160
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['lion','lions']
temp_dict['food'] = 'carnivore'
temp_dict['weight'] = (190+130)/2
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['cow','cows','calf','calves']
temp_dict['food'] = 'herbivore'
temp_dict['weight'] = (1100+720)/2
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['sheep','lamb','lambs']
temp_dict['food'] = 'herbivore'
temp_dict['weight'] = (160+100)/2
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['bear','bears']
temp_dict['food'] = 'carnivore'
temp_dict['weight'] = 110
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['monkey','monkeys']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = 50
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['chimp','chimps','chimpanzee','chimpanzees']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = 50
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['tiger','tigers']
temp_dict['food'] = 'carnivore'
temp_dict['weight'] = (310+170)/2
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['giraffe','giraffes']
temp_dict['food'] = 'herbivore'
temp_dict['weight'] = (1200+830)/2
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['dog','dogs','puppy','puppies','doggy','doggies','pup','pups']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = (36+32)/2
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['cat','cats','kitten','kittens','kitty','kitties']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = 4
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['raccoon','raccoons']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = 9
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['wolf','wolves']
temp_dict['food'] = 'carnivore'
temp_dict['weight'] = (80+55)/2
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['bat','bats']
temp_dict['food'] = 'carnivore'
temp_dict['weight'] = 1
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['shark','sharks']
temp_dict['food'] = 'carnivore'
temp_dict['weight'] = 900
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['dragon','dragons']
temp_dict['food'] = 'carnivore'
temp_dict['weight'] = 18000
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['badger','badgers']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = 10
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['meerkat','meerkats']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = 720
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['duck','ducks','duckling','ducklings']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = 1
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['swan','swans','cignet','cignets']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = 10
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['goose','geese','gosling','goslings']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = 5
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['mouse','mice']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = 0.019
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['rat','rats']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = 0.2
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['crocodile','crocodiles']
temp_dict['food'] = 'carnivore'
temp_dict['weight'] = 750
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['alligator','alligators']
temp_dict['food'] = 'carnivore'
temp_dict['weight'] = 200
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['gorilla','gorillas','ape','apes']
temp_dict['food'] = 'herbivore'
temp_dict['weight'] = 160
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['penguin','penguins']
temp_dict['food'] = 'carnivore'
temp_dict['weight'] = 20
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['spider','spiders','tarantula','tarantulas']
temp_dict['food'] = 'carnivore'
temp_dict['weight'] = 0.005
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['eagle','eagles']
temp_dict['food'] = 'carnivore'
temp_dict['weight'] = 5
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['turtle','turtles','tortoise','tortoises']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = 200
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['fox','foxes']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = 8
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['fish']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = 1
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['whale','whales']
temp_dict['food'] = 'carnivore'
temp_dict['weight'] = 1000
list_of_dicts.append(temp_dict)


temp_dict = {}
temp_dict['names']=['wombat','wombats']
temp_dict['food'] = 'herbivore'
temp_dict['weight'] = 30
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['kangaroo','kangaroos','roo']
temp_dict['food'] = 'herbivore'
temp_dict['weight'] = 80
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['frog','frogs','toad','toads']
temp_dict['food'] = 'carnivore'
temp_dict['weight'] = 0.001
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['chicken','chickens','hen','hens','chick','chicks']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = 1
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['hippo','hippos','hippopotamus']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = 1500
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['rhino','rhinos','rhinoceros']
temp_dict['food'] = 'herbivore'
temp_dict['weight'] = 2000
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['camel','camels']
temp_dict['food'] = 'herbivore'
temp_dict['weight'] = 500
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['pig','pigs','piggy','piggies','piglet','piglets','hog','hogs','boar','boars']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = 50
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['ladybird','ladybirds']
temp_dict['food'] = 'carnivore'
temp_dict['weight'] = 0.00002
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['rabbit','rabbits','bunny','bunnies','hare','hares']
temp_dict['food'] = 'herbivore'
temp_dict['weight'] = 1
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['bug','bugs','insect','insects','beetle','beetles']
temp_dict['food'] = 'herbivore'
temp_dict['weight'] = 0.00002
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['unicorn','unicorns']
temp_dict['food'] = 'herbivore'
temp_dict['weight'] = 750
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['horse','horses','pony','ponies']
temp_dict['food'] = 'herbivore'
temp_dict['weight'] = 750
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['hedgehog','hedgehogs']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = 1
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['hamster','hamsters']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = 0.02
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['llama','llamas']
temp_dict['food'] = 'herbivore'
temp_dict['weight'] = 160
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['alpaca','alpacas']
temp_dict['food'] = 'herbivore'
temp_dict['weight'] = 80
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['flamingo','flamingo']
temp_dict['food'] = 'omnivore'
temp_dict['weight'] = 3
list_of_dicts.append(temp_dict)


temp_dict = {}
temp_dict['names']=['deer']
temp_dict['food'] = 'herbivore'
temp_dict['weight'] = 80
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['moose']
temp_dict['food'] = 'herbivore'
temp_dict['weight'] = 600
list_of_dicts.append(temp_dict)

temp_dict = {}
temp_dict['names']=['dragonfly','dragonflies']
temp_dict['food'] = 'carnivore'
temp_dict['weight'] = 0.003
list_of_dicts.append(temp_dict)

db.animals.insert_many(list_of_dicts)
db.animals.update({},{"$set" : {"total_boy_count":0}},upsert=False,multi=True)
db.animals.update({},{"$set" : {"total_girl_count":0}},upsert=False,multi=True)
db.animals.update({}, {'$set': {'retailers': []}},upsert=False,multi=True)
# db.animals.update({}, {'$set': {'retailer.girl_count': 0}},upsert=False,multi=True)
# db.animals.update({}, {'$set': {'retailer.name': ''}},upsert=False,multi=True)

print(db.animals.count())
