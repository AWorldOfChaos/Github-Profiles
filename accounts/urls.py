from django.urls import include, path
from . import views
from django.contrib import admin
from django.conf.urls import url


urlpatterns = [
    path('', views.home),
    path('signup/', views.signup),
    path('login/', views.login_view),
    # path('login/', include('django.contrib.auth.urls'))
    path('site/', views.site_view),
    path('logout/', views.logout_view),
    path('profile/', views.profile_view),
    path('update/', views.update_view),
    path('explore/', views.explore),
    path('explore/<str:account>/', views.explore_view)
]