from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MainUser(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    choice = models.CharField(max_length=10, choices=[('rock', 'Rock'), ('paper', 'Paper'), ('scissors', 'Scissors')])

class SubUser(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    main_user = models.ForeignKey(MainUser, on_delete=models.CASCADE, null=True, related_name='host')
    choice = models.CharField(max_length=10, choices=[('rock', 'Rock'), ('paper', 'Paper'), ('scissors', 'Scissors')])
    result = models.CharField(max_length=10, blank=True, null=True)