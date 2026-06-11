from collections import defaultdict
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Tree(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
        
    def __str__(self):
        return self.name
        
class TreeNode(models.Model):
    name = models.CharField(max_length=100)
    tree = models.ForeignKey(Tree, related_name='nodes', on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='focus_tree/images/%Y/%m/%d')
    main_text = models.CharField(max_length=10000, default='')
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)
    parents = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='children',
        through='NodeRelation',
        through_fields=('child', 'parent')
    )

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "Tree Node"
        verbose_name_plural = "Tree Nodes"

    def get_ancestors(self):
        ancestors = []
        nodes_to_visit = list(self.parents.all())
        while nodes_to_visit:
            node = nodes_to_visit.pop(0)
            if node not in ancestors:
                ancestors.append(node)
                nodes_to_visit.extend(node.parents.all())
        return ancestors

    def get_descendants(self):
        descendants = []
        nodes_to_visit = list(self.children.all())
        while nodes_to_visit:
            node = nodes_to_visit.pop(0)
            if node not in descendants:
                descendants.append(node)
                nodes_to_visit.extend(node.children.all())
        return descendants

class NodeRelation(models.Model):
    tree = models.ForeignKey(Tree, related_name='edges', on_delete=models.CASCADE, null=True)
    parent = models.ForeignKey(TreeNode, related_name='parent_relations', on_delete=models.CASCADE)
    child = models.ForeignKey(TreeNode, related_name='child_relations', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.parent}->{self.child}'
        
    class Meta:
        unique_together = ('parent', 'child')

    def save(self, *args, **kwargs):
        if NodeRelation.objects.filter(parent=self.parent, child=self.child).exists():
            raise ValidationError('A NodeRelation with this parent and child already exists.')
        super().save(*args, **kwargs)