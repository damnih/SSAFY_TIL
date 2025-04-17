from django.shortcuts import redirect, render
from .forms import ArticleForm, CommentForm
from .models import Article, Comment


def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = article.comment_set.all()
    context = {
        'article': article,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'articles/detail.html', context)


def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)


def delete(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.user:
        article.delete()
    return redirect('articles:index')


def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:index')
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/update.html', context)


def comments_create(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()
        return redirect('articles:detail', article.pk)
    context = {
        'comment_form': comment_form,
    }
    return render(request, 'articles/detail.html', context)


def comments_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('articles:detail', article_pk)


def likes(request, article_pk):
    # 좋아요를 누를 게시글이 어떤건지 조회 
    article = Article.objects.get(pk=article_pk)

    # 좋아요 추가 / 좋아요 취소 
    # 언제 추가하고 취소할지 분간 어케함? 
    # 바로 과거에 좋아요를 한 적이 있다면-> 취소. 아니라면-> 좋아요
    # 좋아요를 요청하는 주체는 request.user 
    # 
    # 만약 특정 게시글에 좋아요를 누른 유저 목록에 현재 요청하는 유저가 있다면? 
    # -> 
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
        # 아니면 유저 측에서 이걸 해도 됨
        request.user.like_articles.remove(article)
        # 다대다는 어느 방향에서 가든 ㄱㅊㄱㅊ 
    else:
        article.like_users.add(request.user)
        request.user.like_articles.add(article)
    return redirect('aritcles:index')
