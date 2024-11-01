from tempfile import template

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import RulesView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('rules/', RulesView.as_view(), name='rules'),
]