from django.urls import path
from articles import views

# 유알엘 이름들을 지정해줬던 건 
# 주로 템플릿에서 주소를 편하게 써주기 위해서였는데
# 우리는 오늘부터 이제 템플릿은 안갈거잖아 걍 백엔드로서 json만 처리할거잖아 
# 그래서 이름들 지정할 필요가 없엉 ㅋ 

urlpatterns = [
    path('articles/', views.article_list), 
    path('articles/<int:article_pk>/', views.article_detail), 
]



