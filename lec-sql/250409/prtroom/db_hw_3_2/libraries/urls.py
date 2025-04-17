from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'libraries'

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index , name='index'),
    path('<int:aut_pk>/', views.detail , name='detail'),
]

