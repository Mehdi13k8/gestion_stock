'''from django.forms import ModelForm
from gestion_stock.models import Comment'''

'''class ImgaccueilForm(ModelForm):
    class Meta:
        model = imgaccueil
        fields = ['photo']'''

'''class MyCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'text', 'notes']'''

from django import forms
from django.forms import ModelForm

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

from .models import menuimages

class PostForm(ModelForm):
    class Meta:
        model = menuimages
        fields = ['cover1', 'cover2', 'cover3', 'cover4', 'cover5', 'cover5', 'cover6', 'cover7', 'cover8',
                  'cover9', 'cover10', 'cover11', 'cover12', 'cover13', 'cover14']
