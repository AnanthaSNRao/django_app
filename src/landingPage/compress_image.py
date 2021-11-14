from PIL import Image
import numpy as np
from django.conf import settings
from landingPage import load_image_db
from sklearn.cluster import KMeans

def compress(image_path):
    name = image_path.split('/')[-1]
    img = np.asarray(Image.open(image_path))
    img_data = (img / 255.).reshape(-1, 3)
    
    kmeans =  KMeans(16).fit(img_data)
    k_colors = kmeans.cluster_centers_[kmeans.predict(img_data)]

    k_img = np.array(k_colors*255, dtype=np.uint8).reshape((img.shape))

    compressed_img = Image.fromarray(k_img)
    
    path = settings.MEDIA_ROOT
    new_name = 'compresssed_'+ name
    compressed_img.save(path+'/'+ new_name)
    w, h, d = img.shape
    try:
        load_image_db.loadImageToDB(path+'/'+ name, 'Un-compressed' ,w, h, d)
        load_image_db.loadImageToDB(path+'/'+ new_name, 'compressed' ,w, h, d)
    except:
        raise('Unable to load image to db')
    return new_name