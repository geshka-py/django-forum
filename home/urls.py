from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('publication/<str:slug>', single_publication, name='publication'),
    path('create_publication/', create_publication, name='create_publication'),
    path('tags/', tags_list, name='tags_list'),
    path('tag/<str:slug>', tag_detail, name='tag_detail'),
    path('search/', search, name='search'),
    path('tag_search/', tag_search, name='tag_search')
]
