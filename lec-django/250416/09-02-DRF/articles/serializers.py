from rest_framework import serializers 
from .models import Article, Comment


# 게시글의 일부 필드를 직렬화 하는 클래스
class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content',)


# 게시글의 전체 필드를 직렬화 하는 클래스
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

# 댓글의 전체 필드를 직렬화하는 클래스 
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        # 외래키 필드를 유효성 검사 목록에서 빼줘야 함 
        # 유효성 검사는 외부에서 터질 수도 잇음 



# 게시글의 전체 필드를 직렬화 하는 클래스
class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        
        
    # 새로운 필드 생성 
    # 댓글 개수를 담기 위한 새로운 필드인 거임
    num_of_comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = '__all__'

    # Serial
    def get_num_of_comments(self, obj):
        # 여기서 obj는 특정 게시글 인스턴스(3번 게시글이면 3번 객체)
        # view 함수에서 annotate해서 생긴 새로운 속성 결과를 사용할 수 잇게 됨
        return obj.num_of_comments
    


