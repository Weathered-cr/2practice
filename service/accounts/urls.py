from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static


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
    path('applications/delete/<int:application_id>/', views.delete_application, name='delete_application'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)