from django import forms
from .models import Post

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image']