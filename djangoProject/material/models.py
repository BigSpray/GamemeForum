from django.db import models

# Create your models here.


# Create your models here.
class images(models.Model):
    img = models.ImageField(upload_to='material_img')


class videos(models.Model):
    video = models.ImageField(upload_to='material_video')


class comment(models.Model):
    blog_id = models.IntegerField()
    content = models.TextField()
    last_edit_time = models.DateTimeField(auto_now=True)
    user_id = models.IntegerField()
    father_id = models.IntegerField(default=0)


class feedback(models.Model):
    name = models.TextField()
    content = models.TextField()
    last_edit_time = models.DateTimeField(auto_now=True)


class AIRVC(models.Model):
    content = models.TextField()
    audio = models.FileField(upload_to='RVC')
