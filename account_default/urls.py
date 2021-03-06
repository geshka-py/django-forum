from django.contrib.auth import views
from django.urls import path
from .views import *


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change', views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('sign_up', registration, name='sign_up'),
    path('profile', profile, name='profile'),
    path('sign_up_res', signup_res, name='signup_res'),
    path('delete/<int:pid>', delete_publication, name='delete'),
    path('edit/<int:pid>', edit_publication, name='edit'),
    path('admin_profile_access/<int:uid>', admin_profile_access, name='admin_profile_access'),
    path('users_list/', users, name='users_list'),
    path('create_user_publication/<int:uid>', create_user_publication, name='create_user_publication')
]
