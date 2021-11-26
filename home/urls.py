from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('publication/<int:pid>', single_publication, name='publication'),
    path('create_publication/', create_publication, name='create_publication'),
    path('tag_publications/<int:tid>', tag_search, name='tag_search'),
    path('search/', search, name='search'),
    path('tag_cloud/', tag_cloud, name='tag_cloud'),
]
