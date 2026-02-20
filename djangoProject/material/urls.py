from django.urls import path
from .views import uploadimg, uploadvideo, getimages, getvideos, deleteimg, deletevideo, getcomments, addcomment, \
    deletecomment, addfeedback, getfeedbacks, get_airvcs, delete_airvc, create_airvc

urlpatterns = [
    path('uploadimg/', uploadimg, name='uploadimg'),
    path('uploadvideo/', uploadvideo, name='uploadvideo'),
    path('getimages/', getimages, name='getimages'),
    path('getvideos/', getvideos, name='getvideos'),
    path('deleteimg/', deleteimg, name='deleteimg'),
    path('deletevideo/', deletevideo, name='deletevideo'),
    path('getcomments/', getcomments, name='getcomments'),
    path('addcomment/', addcomment, name='addcomment'),
    path('deletecomment/', deletecomment, name='deletecomment'),
    path('addfeedback/', addfeedback, name='addfeedback'),
    path('getfeedbacks/', getfeedbacks, name='getfeedbacks'),
    path('airvc_get_all/', get_airvcs, name='get-all-airvcs'),
    path('airvc_create/', create_airvc, name='create-airvc'),
    path('airvc_delete/', delete_airvc, name='delete-airvc'),
]
