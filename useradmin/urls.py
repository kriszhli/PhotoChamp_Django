from django.urls import path
from . import views

app_name = 'useradmin'

urlpatterns = [
    path('login/', views.auth_view, name='login'),
    path('register/', views.auth_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_detail_view, name='profile'),
    path('profile/edit/', views.profile_update_view, name='profile_edit'),
]
