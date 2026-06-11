from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from unidecode import unidecode
# Create your models here.
class Post(models.Model):
    class Meta:
        ordering = ["-id"]#최신순 정렬
        indexes = [
            models.Index(fields=['slug']),
        ]

    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def custom_slugify(self, value):
        value = unidecode(value)
        return slugify(value)
        
    def save(self, *args, **kwargs):
        if not self.slug:
            
            base_slug = self.custom_slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_app:read_post', kwargs={'slug':self.slug})
        
    def __str__(self):
        return self.title

class Content(models.Model):
    POST_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('youtube', 'Youtube'),
    )
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='contents')
    content_type = models.CharField(max_length=50, choices=POST_TYPES)
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='post_images/%Y/%m/%d', blank=True)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.content_type} - {self.post.title}"

