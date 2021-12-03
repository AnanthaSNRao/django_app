
from pymongo import MongoClient
from django.conf import settings
import datetime
import pymongo

from scipy.sparse import data

client = MongoClient("mongodb+srv://Anantha_sn:Anantha_sn@cluster0.kyfuw.mongodb.net/test?retryWrites=true&w=majority")

def loadImageToDB(imagePath, type ,w, h, d, s=0):
    db = client.get_database('test')
    

    with open(imagePath, mode='rb') as file:
        img = file.read()

    col = db['image']
    ratio = round(s/len(img),2) 
    image = {'image': img, 'type': type, 'name': imagePath.split('/')[-1], 'datetime': datetime.datetime.now(), 'width': w, 'hieght': h, 'depth': d, 'size': len(img), 'ratio': ratio, 'ar': get_aspect_ratio(h,w)}
    id = col.insert_one(image).inserted_id
    image['id'] =  id
    return image

def getImageFromDB(name):
    print(name)
    db = client.get_database('test')
    col = db['image']
    data = col.find_one({'name':name})['image']
    path = settings.MEDIA_ROOT
    
    with open(path+'/'+name, "wb+") as fh:
         fh.write(data)
    return data

def get_aspect_ratio(h, w):
    ar = w/h

    if ar == (4/3):
        return '4:3'

    elif ar == 1:
        return '1:1'
    elif ar == (16/9):
        return '16:9'
    else:
        return str(round(ar,2))+":1"

def get_list_():
    db = client.get_database('test')
    col = db['image']
    
    data = []
    size = 0
    com_size =0

    for x in col.find({},{'image':0, 'datetime':0}).sort([("_id", pymongo.DESCENDING)]):
        data.append(x)
        if x['type'] == 'Un-compressed':
            size+= x['size']
        else:
            com_size+=x['size']
    print(data[0])
    # data.sort(key=lambda x: x['_id'])
    return data, size, com_size
