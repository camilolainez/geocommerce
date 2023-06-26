from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
import users.views as userviews

#views
urlpatterns = [
    
    path('admin/', admin.site.urls),

    #index
    path('', views.AboutTemplateView.as_view(), name='index'),

    #users
    # path('register/', views.UserRegisterView.as_view(), name='register'),
    path('users/', include('users.urls')),
    # path('logout/', views.UserLogoutView.as_view(), name='logout'),

    #gencast
    path('gencast/', include('gencast.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
