from django.urls import path

from . import views

app_name = 'formsapp'
urlpatterns = [
    path('form-1/', views.form1, name='form1'),
    path('form-2/', views.form2, name='form2'),
    path('form-3/', views.form3, name='form3'),
    path('form-4/', views.form4, name='form4'),
    path('form-5/', views.form5, name='form5'),
]
