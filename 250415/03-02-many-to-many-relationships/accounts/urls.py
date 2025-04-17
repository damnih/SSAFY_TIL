from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('profile/<username>/', views.profile, name='profile'),
    # 이 variable routing은 str이 기본값이어서 str은 생략해도 됨 ㅇㅇ 
    # 아래와 같은 코드임 
    # path('profile/<str:username>/', views.update, name='update'),
    # cf. 왜 앞에 프로필을 붙였느냐?
    # 만약 없이 그대로 쓰잖아? 얘는 문자열 variable routing이기 때문에 다른 로그인, 로그아웃 같은 주소들도 다 변수 라우팅으로 인식하게 됨 
    # 그래서 이하 달리는 주소가 전부 씹혀버림,,
    # 위험해,,
    # 그래서 문자열 변수 라우팅은 맨마지막에 써줘야함
    # path('<str:username>/', views.update, name='update'),    
    path('<int:user_pk>/follow/', views.follow, name='follow'),
]


