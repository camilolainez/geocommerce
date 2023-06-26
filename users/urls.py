from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.users_root, name='users_root'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout' ),
    path('register/', views.register_view, name='register'),
    path('check-username/', views.check_username, name='check_username')
    # Otras URLs específicas de la aplicación 'accounts'
]