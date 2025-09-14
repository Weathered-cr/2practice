from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    # Аккаунты
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('rules/', views.RulesView.as_view(), name='rules'),

    # Заявки (внутри accounts)
    path('applications/', views.view_applications, name='view_applications'),
    path('applications/create/', views.create_application, name='create_application'),
    path('applications/<int:pk>/update-status/', views.update_status, name='update_status'),
    path('applications/delete/<int:application_id>/', views.delete_application, name='delete_application'),

    path('categories/', views.manage_categories, name='manage_categories'),
    path('categories/<int:pk>/delete/', views.delete_category, name='delete_category'),
]
