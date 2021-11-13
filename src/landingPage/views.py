from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from landingPage.forms import Image
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from landingPage import compress_image 

# Create your views here.
def default_view(request, *args, **kwagrs):
    return render(request, "home.html", {})
@csrf_exempt
def getImage(request, *args, **kwargs):
    
    if request.method == "POST":
        f = request.FILES['file']
        name = request.POST.get('file','old_image.jpeg')
        if f:
             p = settings.MEDIA_ROOT
             url = handle_uploaded_file(f,p+'/'+name)
             return render(request, "home.html", {'url':url})
        else:
            return render(request, "home.html", {})
    else:
        return render(request, "home.html", {})

def handle_uploaded_file(f, name):
    # p = settings.MEDIA_ROOT
    fs = FileSystemStorage()
    filename = fs.save(name, f)
    uploaded_file_url = fs.url(filename)
    compress_image.compress(filename)
    return uploaded_file_url
    