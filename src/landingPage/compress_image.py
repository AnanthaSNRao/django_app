from PIL import Image
import numpy as np
from django.conf import settings
from landingPage import load_image_db
from sklearn.cluster import KMeans

def compress(image_path):
    name = image_path.split('/')[-1]
    img = np.asarray(Image.open(image_path))
    img_data = (img / 255.).reshape(-1, 3)
    print(type(img_data), img_data.dtype)
    
    kmeans =  KMeans(30).fit(img_data)
    k_colors = kmeans.cluster_centers_[kmeans.predict(img_data)]
    print(type(k_colors), k_colors.dtype)
    k_img = np.array(k_colors*255, dtype=np.uint8).reshape((img.shape))
    print(type(k_img), k_img.dtype)
    compressed_img = Image.fromarray(k_img)
    
    path = settings.MEDIA_ROOT
    new_name = 'compressed_'+ name
    compressed_img.save(path+'/'+ new_name)
    image = {}
    c_image = {}
    w, h, d = img.shape
    try:
        image = load_image_db.loadImageToDB(path+'/'+ name, 'Un-compressed' ,w, h, d)
        c_image = load_image_db.loadImageToDB(path+'/'+ new_name, 'compressed' ,w, h, d, image['size'])
    except Exception as err:
        print(err)
        raise('Unable to load image to db')
    return image, c_image