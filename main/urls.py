from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('add_job/', views.add_job, name='add_job'),
    path('jobs/', views.show_jobs, name='jobs'),
    path('toggle-role/', views.toggle_role, name='toggle_role'),
]
