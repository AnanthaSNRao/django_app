from PIL.Image import NONE
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from landingPage.forms import Image
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from landingPage import compress_image, load_image_db
import os

# Create your views here.
def default_view(request, *args, **kwagrs):
    return render(request, "home.html", {})
@csrf_exempt
def getImage(request, *args, **kwargs):
    
    if request.method == "POST":
        f = request.FILES['file']
        name = f.name
        if f:
            # delete_files_cache()
            try:
                p = settings.MEDIA_ROOT
                url, image, c_image = handle_uploaded_file(f,p+'/'+name)
                image['size'] = get_size(image['size'])
                c_image['size'] = get_size(c_image['size'])
                
                return render(request, "home.html", {'url':url, 'image': image, 'c_image': c_image})
            except Exception as err:
                print(err)
                return render(request, "home.html", {'error': err})
        else:
            return render(request, "home.html", {})
    else:
        return render(request, "home.html", {})

def delete_files_cache():
    path = settings.MEDIA_ROOT
    os.remove(path+'/*')
    return

@csrf_exempt
def download(request, *args, **kwagrs):
    name = request.POST.get('text')
    file_path = os.path.join(settings.MEDIA_ROOT, name)
    load_image_db.getImageFromDB(name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="image/*")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def get_list(request, *args, **kwagrs):
    data, s, cs = load_image_db.get_list_()
    print(len(data))
    s= get_size(s)
    cs = get_size(cs)
    return render(request, "list.html", {'data': data, 'size': s, 'csize': cs})


def handle_uploaded_file(f, name):
    
    fs = FileSystemStorage()
    filename = fs.save(name, f)
    name = name.split('/')[-1]
    uploaded_file_url = fs.url(name)
    image, c_image = compress_image.compress(filename)
    return uploaded_file_url, image, c_image

def get_size(size):
    unit ='KB'
    size = int(size)/1000
    if size >= 1000:
        size = size/1000
        unit = 'MB'
    return str(round(size,2)) +" "+ unit