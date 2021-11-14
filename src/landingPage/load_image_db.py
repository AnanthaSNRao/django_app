
from pymongo import MongoClient
from django.conf import settings
import datetime

client = MongoClient("mongodb+srv://Anantha_sn:Anantha_sn@cluster0.kyfuw.mongodb.net/test?retryWrites=true&w=majority")

def loadImageToDB(imagePath, type ,w, h, d):
    db = client.get_database('test')
    

    with open(imagePath, mode='rb') as file:
        img = file.read()

    col = db['image']

    image = {'image': img, 'type': type, 'name': imagePath.split('/')[-1], 'datetime': datetime.datetime.now(), 'width': w, 'hieght': h, 'depth': d, 'size': len(img)}
    id = col.insert_one(image).inserted_id
    return id

def getImageFromDB(name):
    print(name)
    db = client.get_database('test')
    col = db['image']
    data = col.find_one({'name':name})['image']
    path = settings.MEDIA_ROOT
    
    with open(path+'/'+name, "wb+") as fh:
         fh.write(data)

