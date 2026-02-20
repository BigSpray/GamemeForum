from django.db import models


# Create your models here.
class blogtype(models.Model):
    type = models.CharField(max_length=50)


class blog(models.Model):
    title = models.TextField()
    img = models.ImageField(upload_to='blog_img', blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=50, default='default_type')
    content = models.TextField()
    view = models.IntegerField(default=0)  # 浏览
    # like = models.IntegerField(default=0)  # 点赞
    collection = models.IntegerField(default=0)  # 收藏
    video = models.FileField(upload_to='blog_video', blank=True, null=True)  # 添加 video 字段
    forblog = models.CharField(max_length=50, default='default_forblog')
    last_edit_time = models.DateTimeField()
    recommend = models.IntegerField(default=0)  # 推荐
    horse = models.IntegerField(default=0)  # 走马灯

    def __str__(self):
        return self.title

    def increase_view(self):
        self.view += 1
        self.save()
