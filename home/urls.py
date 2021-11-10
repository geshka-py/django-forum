from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('publication/<int:pid>', single_publication, name='publication'),

    path(r'publication_relation', UserPublicationRelationView),
]
