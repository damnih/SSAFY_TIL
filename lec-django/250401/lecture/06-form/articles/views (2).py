from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm 



# 메인 페이지를 응답하는 함수 (+ 전체 게시글 목록)
def index(request):
    # DB에 전체 게시글 요청 후 가져오기
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


# 특정 단일 게시글의 상세 페이지를 응답 (+ 단일 게시글 조회)
def detail(request, pk):
    # pk로 들어온 정수 값을 활용 해 DB에 id(pk)가 pk인 게시글을 조회 요청 
    article = Article.objects.get(pk=pk)
    context = {
        'article': article,
    }
    return render(request, 'articles/detail.html', context)


# 게시글을 작성하기 위한 페이지를 제공하는 함수
def new(request):
    form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)


def create(request):
    # 1. 요청 메서드가 POST라면 
    if request.method == 'POST':
        # 1.1 사용자로부터 받은 데이터를 인자로 통째로 넣어서 form 인스턴스 생성
        form = ArticleForm(request.POST)
        # 1.2 데이터가 유효한지 검사(유효성 검사)
        if form.is_valid(): 
            # 1.3 유효성 검사가 통과한다면 저장장
            # 유효성 검사를 통과했다면, (데이터 저장)
            article = form.save() # save는 반환값이 잇음 # 그걸 article에 담아주면 됨됨
            # 1.4 상세 페이지로 리다이렉트 
            return redirect('articles:detail', article.pk)
        
    # 2. 요청 메서드가 POST가 아니라면
    # 즉 GET, PUT, DELETE 등의 메서드들
    # 근데 우리한테 중요한 건 이 생성 쪽에서 POST를 쓴다는 점임 
    # 그래서 POST로 먼저 끊어놓고 이외로 구분했는지 나오는 것!!!! 

    else: 
        # 2.1 ArticleForm 인스턴스를 생성성
        form = ArticleForm()
    # case 1 : 1.2에서 내려왔을 때 : 에러메세지를 담은 form 
    # case 2 : 2.1이 끝나고 내려왔을 때 : 빈 form 
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)


# # 사용자로부터 데이터를 받아 저장하고 저장이 완료되었다는 페이지를 제공하는 함수
# def create(request):
#     # 사용자로 부터 받은 데이터를 추출
#     # title = request.POST.get('title')
#     # content = request.POST.get('content')
    
#     # 사용자로부터 받은 데이터를 인자로 통째로 넣어서 form 인스턴스 생성 
#     form = ArticleForm(request.POST)

#     # 데이터가 유효한지 검사(유효성 검사)
#     if form.is_valid():
#         # 유효성 검사를 통과했다면, (데이터 저장)
#         article = form.save() # save는 반환값이 잇음 # 그걸 article에 담아주면 됨됨
#         return redirect('articles:detail', article.pk)
#     # 통과하지 못했다면, 
#     # 현재 사용자가 게시글을 작성하는 템플릿(new 페이지)을 다시 한번 응답 
#     context = {
#         # 왜 유효성 검사를 통과하지 못했는지에 대한 에러메시지를 담고 있음
#         'form': form, 
#     }
#     return render(request, 'articles/new.html', context)

#     # DB에 저장 요청 (3가지 방법)
#     # 1.
#     # article = Article()
#     # article.title = title
#     # article.content = content
#     # article.save()

#     # 2.
#     # article = Article(title=title, content=content)
#     # article.save()
    
#     # 3.
#     # Article.objects.create(title=title, content=content)
#     # return render(request, 'articles/create.html')
#     # return redirect('articles:index')
#     return redirect('articles:detail', article.pk)


def delete(request, pk):
    # 어떤 게시글을 지우는지 먼저 조회
    article = Article.objects.get(pk=pk)
    # DB에 삭제 요청
    article.delete()
    return redirect('articles:index')


def update(request, pk):
    article = Article.objects.get(pk=pk)

    if request == 'POST':
        form = ArticleForm(request.POST, instance=article) 

        if form.is_valid():
            form.save()
            return redirect('articles:detail', article.pk)
     
    else:
        form = ArticleForm(instance=article)


    context = {
        'article': article, 
        'form': form,
    }

    return render(request, 'articles:detail', context)


# def edit(request, pk):
#     # 몇번 게시글 정보를 보여줄지 조회
#     article = Article.objects.get(pk=pk)
#     form = ArticleForm(instance=article)
#     context = {
#         'article': article,
#         'form': form,
#     }
#     return render(request, 'articles/edit.html', context)


# def update(request, pk):
#     # 어떤 글을 수정하는지 먼저 조회
#     article = Article.objects.get(pk=pk)

#     # 사용자가 쓴 걸 그대로 form인스턴스 생성 
#     form = ArticleForm(request.POST, instance=article) 

#     if form.is_valid():
#         form.save()
#         return redirect('articles:detail', article.pk)
    
#     context = {
#         'article': article, 
#         'form': form, 

#     }

#     # 사용자 입력 데이터를 기존 인스턴스 변수에 새로 갱신 후 저장
#     # article.title = request.POST.get('title')
#     # article.content = request.POST.get('content')
#     # article.save()
#     return render('articles:detail', article.pk, context)


