from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField()
    image = models.ImageField(upload_to='photos/')
    timestamp = models.DateTimeField(auto_now_add=True)
    moderation_status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f'Photo {self.id}'