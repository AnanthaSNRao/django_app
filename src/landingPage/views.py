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
                url, cname = handle_uploaded_file(f,p+'/'+name)
                return render(request, "home.html", {'url':url, 'cname': cname})
            except Exception:
                return render(request, "home.html", {'error': args})
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

def handle_uploaded_file(f, name):
    
    fs = FileSystemStorage()
    filename = fs.save(name, f)
    name = name.split('/')[-1]
    uploaded_file_url = fs.url(name)
    cname = compress_image.compress(filename)
    return uploaded_file_url, cname
    