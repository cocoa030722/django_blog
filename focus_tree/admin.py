from django.contrib import admin

from .models import TreeNode, NodeRelation, Tree
# Register your models here.
admin.site.register(Tree)
admin.site.register(TreeNode)
admin.site.register(NodeRelation)