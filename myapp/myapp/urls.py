"""
URL configuration for myapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static  # ✅ Import this
from django.urls import path,include
from django.contrib.auth.views import LogoutView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('login/', views.login, name='login'),
    path('signup/',views.SignUpView.as_view(), name='SignUp'),
    # path("accounts/", include("django.contrib.auth.urls")),
    path('logout/', views.logout_view, name='logout'),  # Use custom view
    path('information/', views.information, name='information'),
    path('add_game/', views.add_game, name='add_game'), 
    path('delete_game/<str:game_id>/', views.delete_game, name='delete_game'),
    path('edit_game/<int:game_id>/', views.edit_game, name='edit_game'),  # Add this
    path('save-game-order/', views.save_game_order, name='save_game_order'),
    path('delete_account/', views.delete_account, name='delete_account'),  
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'myapp' / 'static')
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)