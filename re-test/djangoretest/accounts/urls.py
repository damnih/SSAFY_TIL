from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('follow/<int:user_pk>/', views.follow, name='follow'),
    path('following/<int:user_pk>/', views.following, name='following'),
    path('followers/<int:user_pk>/', views.followers, name='followers'),
]
