
from django.urls import path, include
from . import views as users_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', users_view.get_home, name='users-home'),
    path('register/', users_view.create_user, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="login"), name='logout'),
    path('profile/', users_view.show_profile, name='user-profile'),
    path('edit-profile/', users_view.edit_profile, name='edit-profile'),
    path('user-delete/', users_view.delete_user, name='user-delete'),
    path('songs/', include('songs.urls')),
    path('playlists/', include('playlists.urls')),
    path('image/', include('Image.urls')),
    path('error/<str:error>', users_view.show_error, name='error-page'),
]
