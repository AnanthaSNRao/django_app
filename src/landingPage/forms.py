from django import forms  
class Image(forms.Form):
    file = forms.FileField() # for creating file input  