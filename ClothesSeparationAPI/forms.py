from django import forms

from .models import Image

class UploadForm(forms.ModelForm):
    
    class Meta:
        model = Image
        fields = {'image'}