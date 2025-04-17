from rest_framework import serializers 
# from rest_framework.decorators import api_view
from .models import Article 


# 직렬화 = serialize 
# 전체 게시글 데이터를 직렬화하는 클래스 

# 여기서 지정한 내용들만이 포스트맨에 출력이 됨
# 애초에 이 필드에 넣은 넘들만 직렬화되는거임
# 다른 정보들은 애초에 직렬화되지 않아서 유효성 검사도 안 치름 
# 쨌든 얘는 도구라는 거임

# 게시글의 일부 필드를 직렬화하는 클래스 
class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article 
        # GET요청으로 게시글 조회를 해보려고 하는데,, all을 하면 너무 뭐가 많아 
        # 이걸 좀 걸러서 볼수잇는 정보를, 데이터 구성을 좀 조정하고 싶어 
        # fields = '__all__'
        # 직렬화 할 때 직렬화 할 필드만 지정을 해줄 수 있음 
        fields = ("id", "title", "content",)



# 시리얼라이저는 내 입맛대로 계속 만들어줄수잇음 이름만 바꿔주면됨

# 게시글의 전체 필드를 직렬화하는 클래스 
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article 
        fields = '__all__'
