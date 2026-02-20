from django.contrib import admin
from .models import blog, blogtype


# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'img', 'name', 'type', 'content', 'view', 'collection', 'video',
                    'forblog', 'last_edit_time', 'recommend', 'horse']


class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']


admin.site.register(blog, BlogAdmin)
admin.site.register(blogtype, BlogTypeAdmin)

