from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.hello),
    path('register/', views.register),
    path('login/', views.logging),
    path('myProfile/', views.my_profile),
    path('profile/<int:other_user_id>/', views.profile),
    path('addPhoto/', views.add_photo),
    path('logout/', views.logout_view),
    path('photo/<int:photo_id>/', views.get_photo),
    path('photoMeta/<int:photo_id>/', views.get_photo_meta),
    path('allPhotos/', views.all_photos),
    path('users/', views.get_users),
    path('follow/<int:other_user_id>/', views.follow),
    path('unfollow/<int:other_user_id>/', views.unfollow),
    path('photoMeta/<int:photo_id>/comments/', views.add_comment),
]
