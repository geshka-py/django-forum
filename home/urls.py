from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('<str:ordering>', home, name='home'),
    path('publication/<int:pid>', single_publication, name='publication'),
    path('create_publication/', create_publication, name='create_publication'),
    path('tags/', tags_list, name='tags_list'),
    path('tag/<str:slug>', tag_detail, name='tag_detail'),
    path('search/', search, name='search'),
    path('tag_search/<str:slug>', tag_search, name='tag_search'),
    path('like/<int:pid>', like_it, name='like'),
    path('categories/<str:slug>', group_view, name='group'),
    path('upload/', file_upload_view, name='upload'),
]
