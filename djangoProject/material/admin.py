from django.contrib import admin
from .models import images, videos, comment, feedback, AIRVC


# Register your models here.


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'img']


class VideosAdmin(admin.ModelAdmin):
    list_display = ['id', 'video']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'blog_id', 'content', 'last_edit_time', 'user_id', 'father_id']


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'content']


class AIRVCAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'audio']


admin.site.register(images, ImagesAdmin)
admin.site.register(videos, VideosAdmin)
admin.site.register(comment, CommentAdmin)
admin.site.register(feedback, FeedbackAdmin)
admin.site.register(AIRVC, AIRVCAdmin)
