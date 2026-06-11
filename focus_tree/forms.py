from django import forms
from django.forms import ModelForm

from .models import TreeNode

class NodeForm(ModelForm):
    class Meta:
        model = TreeNode
        fields = ['name', 'image', 'main_text', 'position_x', 'position_y']

class TreeForm(forms.Form):
    tree_name = forms.CharField(label='트리 이름을 입력', max_length=255)
    