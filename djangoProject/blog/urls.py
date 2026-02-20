from django.urls import path
from .views import get_blogs, update_blog, deleteblog, get_blogtypes, deletetype, addtype, change_horse_status, addma, \
    change_recommend_status, BlogFavoriteView, viewadd, saveBlog, update_blogs_username, uploadEditorImage

urlpatterns = [
    path('getblogs/', get_blogs, name='get_blogs'),
    path('updateblog/<int:pk>/', update_blog, name='update_blog'),
    path('deleteblog/', deleteblog, name='deleteblog'),
    path('getblogtypes/', get_blogtypes, name='get_blogtypes'),
    path('deletetype/', deletetype, name='deletetype'),
    path('addtype/', addtype, name='addtype'),
    path('change_horse_status/', change_horse_status, name='change_horse_status'),
    path('change_recommend_status/', change_recommend_status, name='change_recommend_status'),
    path('addma/', addma, name='addma'),
    path('blogs/<int:blog_id>/favorite/', BlogFavoriteView.as_view(), name='blog-favorite'),
    path('viewadd/', viewadd, name='viewadd'),
    path('saveBlog/', saveBlog),
    path('updateBlogsUserName/', update_blogs_username, name='update_blogs_username'),
    path('uploadEditorImage/', uploadEditorImage, name='uploadEditorImage'),
]
