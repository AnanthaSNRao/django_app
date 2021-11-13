
from pymongo import MongoClient
from django.conf import settings
import datetime

client = MongoClient("mongodb+srv://Anantha_sn:Anantha_sn@cluster0.kyfuw.mongodb.net/test?retryWrites=true&w=majority")

def loadImageToDB(imagePath):
    db = client.get_database('test')
    

    with open(imagePath, mode='rb') as file:
        img = file.read()

    col = db['image']

    image = {'image': img, 'type': 'Un-compressed', 'name': imagePath[2:], 'datetime': datetime.datetime.now()}
    id = col.insert_one(image).inserted_id
    return id

def getImageFromDB(name):
    db = client.get_database('test')
    col = db['image']
    data = col.find_one({'name':name})['image']
    path = settings.MEDIA_ROOT
    
    with open(path+'/'+name, "wb+") as fh:
         fh.write(data)

