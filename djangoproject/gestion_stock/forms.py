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

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

from .models import imgaccueil

class PostForm(forms.ModelForm):
    class Meta:
        model = imgaccueil
        fields = ['title', 'cover']