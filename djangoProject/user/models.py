from django.db import models


# Create your models here.
class user(models.Model):
    name = models.CharField(max_length=20)
    img = models.ImageField(upload_to='user_img', blank=True, null=True)
    account = models.CharField(max_length=20, default="abc")
    password = models.CharField(max_length=20, default="123")
    myself = models.TextField(max_length=30, default="这个人很懒，没有简介哦~")

    def __str__(self):
        return self.name


class userData(models.Model):
    """
    用户发布的数据内容
    """
    userID = models.ForeignKey(user, on_delete=models.CASCADE, related_name="user_id")
    video = models.FileField(upload_to='video')
    content = models.CharField(max_length=2000)

