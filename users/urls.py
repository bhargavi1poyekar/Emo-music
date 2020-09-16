
from django.urls import path,include
from . import views as users_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',users_view.home,name='users-home'),
    path('register/', users_view.createUser,name="register"),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page="login"),name='logout'),
    path('profile/',users_view.showProfile,name='user-profile'),
    path('edit-profile/',users_view.editProfile,name='edit-profile'),
    path('user-delete/',users_view.deleteUser,name='user-delete'),
]