from django.shortcuts import render
from .models import Article, Comment
from django.db.models import Count


# Create your views here.
def index_1(request):
    # articles = Article.objects.order_by('-pk')
    # -pk는 걍 desc의 뜻임 내림차순의 뜻 
    articles = Article.objects.annotate(Count('comment')).order_by('-pk')
    # annotate 뜻은 주석임 걍 말을 존나해준다는 뜻 
    # 그 게시글들의 댓글을 카운트해서 다 줘 
    # 쿼리를 줄이는 법 걍 처음 말을 ㅈㄴ 길게 해줘서 조건을 잘 걸어주기 ㅋㅋ ㅜㅜ 
    # 
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index_1.html', context)


def index_2(request):
    # articles = Article.objects.order_by('-pk')
    articles = Article.objects.select_related('user').order_by('-pk')
    # N+1 조회라고 생각하면 된대 
    # select_related는 게시글 전체 가져오면서 그에 관련된 user도 같이 가져오겠다는 말임 
    # SQL 쿼리 어케 변했나 보니깐
    # 원래는 11쿼리 있었는데 1개로 줄음 
    #  INNER JOIN "accounts_user" 을 이용하게 됐대!!!! 
    #    
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index_2.html', context)


def index_3(request):
    # articles = Article.objects.order_by('-pk')
    articles = Article.objects.prefetch_related('comment_set').order_by('-pk')
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index_3.html', context)


from django.db.models import Prefetch


def index_4(request):
    articles = Article.objects.order_by('-pk')
    # articles = Article.objects.prefetch_related('comment_set').order_by('-pk')
    articles = Article.objects.prefetch_related(
        Prefetch('comment_set', queryset=Comment.objects.select_related('user'))
    ).order_by('-pk')

    context = {
        'articles': articles,
    }
    return render(request, 'articles/index_4.html', context)
