from django.db import models
from django.contrib.auth.models import User
import uuid
import os

def game_screenshot_path(instance, filename):
    # Generate a UUID for the filename
    ext = filename.split('.')[-1]
    # Create a unique filename using UUID
    filename = f"{uuid.uuid4()}.{ext}"
    # Return the path: game_screenshots/user_id/filename
    return os.path.join('game_screenshots', str(instance.user.id), filename)

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='Games')
    name = models.CharField(max_length=200)
    game_company = models.CharField(max_length=200)
    about = models.TextField()
    realise_date = models.DateField()
    platform = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)  # 1-10
    comment = models.TextField()
    screenshot = models.ImageField(upload_to=game_screenshot_path)
    order = models.IntegerField(default=0) 
    def __str__(self):
        return f"{self.name} - {self.user.username}"
    class Meta:
        ordering = ['order']  # This will order games by this field

