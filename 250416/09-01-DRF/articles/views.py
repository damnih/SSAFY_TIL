from django.shortcuts import render

# 응답에 대한 도구들 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Article
from .serializers import ArticleListSerializer, ArticleSerializer



# Create your views here.
@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        # 일단 아티클들을 다 조회해오고 / 전체 게시글 데이터 조회 
        articles = Article.objects.all()
        # 시리얼라이저 함수도 끌고와서, 아티클즈에 적용시켜 
        # 여기서 many라는 건,, 시리얼라이즈 대상이 쿼리셋인 경우에 입력해주는 인자 

        # 강사님 설명 
        # articles는 장고에서만 쓸 수 있는 쿼리셋 데이터 타입이기 때문에 
        # 우리가 만든 모델시리얼라이저로 변환을 진행해줘야함 
        # 사실상 이 serializer가 변환기라고 생각하면 됨
        # # '다수 데이터'라서 many=True 처리를 해줘야함 
        serializer = ArticleListSerializer(articles, many=True)
        # 그럼 이 적용한 결과값 중 데이터만 추출해서 response로 넘겨줘
        # serialized date 객체에서 실제 데이터를 추출하는 거

        # 강사님 설명 
        # 우리 렌더도 안하고 리다이렉트도 안할거임 
        # 걍 응답이 가는거임
        # DRF에서 제공하는 Response를 사용해 JSON 데이터를 응답 
        # JSON 데이터는 serializer의 데이터 속성에 존재함 
        # serializer는 덩어리임 ㅇㅇ 
        return Response(serializer.data)
    
    # 게시글 생성 요청에 대한 응답
    elif request.method == 'POST':
        # 예전 코드 
        # form = ArticleForm(request.POST)
        # 사용자 입력 데이터를 클래스로 받아서 변환
        serializer = ArticleListSerializer(data=request.data)
        # 그 데이터 유효성 검사 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 유효하지 않다면 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # 이렇게 POST 요청 보고 나니 CRUD에서의 CREATE과 굉장히 유사하지? 
    # 다 맥락이 있는거야~~~ 

        

@api_view(['GET', 'DELETE', 'PUT']) # 데코레이터는 필수 
# 조회, 삭제, 수정
def article_detail(request, article_pk):
#     # 얘 또한 일단 아티클들을 다 조회하고
    article = Article.objects.get(pk=article_pk)
    if request.method == 'GET':
        # 시리얼라이저로 처리를 해줌 ArticleSerializer로 직렬화 해준다는 뜻 
        # 그리고 이 반환을 변수에 담아줌
        serializer = ArticleSerializer(article)
        # 변수에 할당된 내용 중 데이터만을 리스폰스로 넣어줌 
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT':
        # 사용자가 보낸 수정 데이터를 변환
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        # 수정할 아티클 넣어주고, 수정을했다는데이터(PUT형식의리퀘스트안에들어가잇음) 넣어주고,
        # 꼭 제목 내용 아이디 등 모든 정보를 수정해야할 필요가 있는게 아니잖아
        # 부분수정을 가능하게 만들어주려면 partial=True 옵션을 켜줘야함

        # 얘를 유효성 검사 해줘야 해 
        if serializer.is_valid():
            # 통과했다면 저장
            serializer.save()
            # 그럼 수정 성공이니깐 성공했다는 걸 리턴
            return Response(serializer.data)
        
        # 여기로 내려오는 건 유효성 검사 실패한 거잖이 
        # 실패했다면 오류 알려줌 
        # 이건 오류가 떴다는 상태!!!!!! 인 거잖아?? 
        # 오류 상태!!!! 를 띄워주는 거니깐 응답 안에 status가 들어가야하는거임 
        # Response를 이용해서 보내줄건데 
        # 이 응답함수 자체가 status를 품고 있어야 오류가 전달된다는거지!!!  
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    

