from django.urls import path
from . import views
urlpatterns = [
    path('', views.user),
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('home/', views.home, name='home_page'),
]