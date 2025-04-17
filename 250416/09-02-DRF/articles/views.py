from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Article, Comment
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer


# Create your views here.
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        # 전체 게시글 데이터 조회
        articles = Article.objects.all()
        # articles는 django에서는 쓸 수 있는 queryset 데이터 타입이기 때문에
        # 우리가 만든 모델시리얼라이저로 변환 진행
        serializer = ArticleListSerializer(articles, many=True)
        # DRF에서 제공하는 Response를 사용해 JSON 데이터를 응답
        # JSON 데이터는 serializer의 data 속성에 존재
        return Response(serializer.data)

    # 게시글 생성 요청에 대한 응답
    elif request.method == 'POST':
        # 예전 코드
        # form = ArticleFrom(request.POST)
        # 사용자가 보낸 ㅈ데이터를 클래스로 받아서 직렬화
        serializer = ArticleSerializer(data=request.data)
        # 유효성 검사
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'DELETE', 'PUT'])
def article_detail(request, article_pk):
    # 단일 게시글 데이터 조회
    article = Article.objects.get(pk=article_pk)
    if request.method == 'GET':
        # ArticleSerializer 클래스로 직렬화를 진행
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        # 사용자가 보낸 수정 데이터를 직렬화
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        # serializer = ArticleSerializer(instance=article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# 댓글 전체 조회하는 함수 
@api_view(['GET'])
def comment_list(request):
    # 댓글 전체 조회 
    # 커멘트 클래스에 있는 모든 객체 담아주기
    comments = Comment.objects.all()
    # 댓글 데이터를 가공 
    # 시리얼라이저에 인자로 가공할 대상을 넣어줌,
    # 근데 그 가공할 대상이 쿼리셋이라면 many 인자 True로 켜줘야함
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)



@api_view(['GET', 'DELETE', 'PUT'])
def comment_detail(request, comment_pk):
    # 특정 댓글 데이터를 조회
    # 이 댓글 데이터는 조회든 수정이든 삭제든 다 공통적으로 할 일이니깐 여기서 먼저 해줌
    comment = Comment.objects.get(pk=comment_pk)

    if request.method == 'GET':
        # 조회한 단일 댓글 데이터를 직렬화해줌 json으로 ㄱㄱ 
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass



@api_view(['POST'])
def comment_create(request, article_pk):
    # 어떤 게시글에 작성되는 댓글인지 단일 게시글을 조회
    article = Article.objects.get(pk=article_pk)
    # 요 위에 얘는 그니깐 단일 인스턴스인거임 
    # 단일 Article인스턴스라 

    # 사용자가 보낸 댓글 데이터를 활용해 가공
    # 시리얼라이저는 인자로 가공할 데이터를 받아줌!! 
    # 즉 인자 안에 넣어줘야한다는건데!!!!
    # 왜 이건 data=request.data느냐? 
    # 이거는 역직렬화를 해줄 거였어서 그래 

    serializer = CommentSerializer(data=request.data)
    # 그리고 이건 생성하는 거니깐 유효성 검사가 필요함
    if serializer.is_valid(raise_exception=True):
        # 추가 데이터(즉 댓글을 달아줄 게시글의 데이터도 여기선 필요하니깐 ㅇㅇ)는 
        # save메서드의 인자를 활용해 넣어줌
        serializer.save(article=article)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


@api_view(['POST'])
def comment_create(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(article=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # (= return json 데이터 + 응답 상태코드)



# 객체
# - 파이썬의 모든 것은 객체다.

# 인스턴스
# 인스턴스는 객체다. (O)
# 인스턴스는 클래스로 인해 생성된 객체다. (OO)

# a = Aclass()

# a는 Aclass의 인스턴스다.
# a는 객체다.

# MOdelform, 모델 시리얼라이저의 키워드인자 instance는 보통 기존 데이터를 의미미


# 3
# 3은 int라는 내장 클래스의 인스턴스
