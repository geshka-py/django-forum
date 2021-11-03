from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('increase_counter/<int:pk>/', increase_counter, name='increase_counter'),
    path('message/<int:pk>/', message_details, name='message')
]
