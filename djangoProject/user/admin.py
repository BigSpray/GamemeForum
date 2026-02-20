from django.contrib import admin
from .models import user, userData


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'img', 'account', 'password', 'myself']


class UserDataAdmin(admin.ModelAdmin):
    list_display = ['userID', 'content', 'video']


admin.site.register(user, UserAdmin)
admin.site.register(userData, UserDataAdmin)
