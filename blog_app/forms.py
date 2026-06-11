from django import forms

from .models import Post, Content

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title']

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['content_type', 'text', 'image', 'order']

    image = forms.ImageField(required=False)
    text = forms.CharField(widget=forms.Textarea, required=False)