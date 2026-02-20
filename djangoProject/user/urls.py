from django.urls import path
from .views import register, delete, get_users, check_username, update_password, \
    uploadAvatar, updateUserInfo, update_myself

urlpatterns = [
    path('register/', register, name='register'),
    path('delete/', delete, name='delete'),
    path('getusers/', get_users, name='get_users'),
    path('checkUsername/', check_username, name='check_username'),
    path('updateUserInfo/', updateUserInfo, name='update_user_info'),
    path('updatePassword/', update_password, name='update_password'),
    path('uploadAvatar/', uploadAvatar, name='uploadAvatar'),
    path('updateMyself/', update_myself, name='update-myself'),
]
