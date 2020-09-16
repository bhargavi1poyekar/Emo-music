
from django.urls import path,include
from . import views as users_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', users_view.createUser,name="register"),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page="login"),name='logout'),
    path('',users_view.home,name='users-home'),
    
    
]