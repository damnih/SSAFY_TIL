from django.shortcuts import render, redirect
from .models import Article
from .forms import ArticleForm


def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article,
    }
    return render(request, 'articles/detail.html', context)


def create(request):
    if request.method == 'POST':
        # form = ArticleForm(request.POST, files=request.FILES)  # 첫번째 인자는 데이터 두번쨰 인자는 파일
        form = ArticleForm(request.POST, request.FILES)  # 위치인자의 위치 맞기 때문에 키워드인자 없어도됨 
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk) 
        # # # 나 질문!! 이거 articles:detail의 detail이 함수인거지? 
        # 아티클이라는 앱 안에 있는 디테일이란 함수(views파일에서 작성됨)를 실행시키겠다는 그런 경로인 거 맞지?!?!?! 
    else:
        form = ArticleForm()
        
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)


def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('articles:index')


def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article )
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/update.html', context)
