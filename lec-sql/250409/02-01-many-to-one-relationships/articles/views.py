from django.contrib.auth.decorators import login_required
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
    # 디테일 페이지에서 수행할 행동이니깐 댓글을 보고자 하는 행동도 여기서 수행
    # 특정 게시글에 작성된 모든 댓글 조회(역참조)
    # 전부다 조회하고 반환된걸 이 comments 변수에 담아줌 
    comments = article.comment_set.all() 

    context = {
        'article': article,
        'comment_form': comment_form, 
        'comments': comments, 
    }
    return render(request, 'articles/detail.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)


@login_required
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('articles:index')


@login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
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
    return render(request, 'articles/update.html', context)


def comments_create(request, article_pk):
    # 어떤 게시글에 작성되는 댓글인지 알려면 게시글을 먼저 조회를 해야함 
    article = Article.objects.get(pk=article_pk)
    # CommentFrom을 활용한 댓글 생성
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        # 외래키 데이터를 넣으려면 댓글 인스턴스가 필요한데,, 
        # 댓글 인스턴스는 save() 호출이 완료되어야 반환됨

        comment = comment_form.save(commit=False)
        # (commit=False) 기본값은 이게 True인데 False로 바꿔주면
        # 댓글 인스턴스는 생성해주지만 실제 DB에 아직 저장 요청은 안보내게 되는거임
        # 약간 깃 애드까지해서 SA에 올리는 느낌 아직 커밋에 푸시까지는 안 한 느낌 
        
        # 여기까지 잘 나왔으니깐,, 
        comment.article = article
        comment.save()
        return redirect('articles:detail', article.pk)
    context = {
        'comment_form': comment_form,
    }
    return render(request, 'articles/detail.html', context)

def comments_delete(request, article_pk, comment_pk):
    # 어떤 댓글이 삭제되는 것인지 조회 
    comment = Comment.objects.get(pk=comment_pk)
    # article_id = comment.article.pk
    # # 댓글 삭제 
    comment.delete()
    # 첫번째 방법에 대한 리턴
    # return redirect('articles:detail', article_id )

    # 두번째 방법
    return redirect('articles:detail', article_pk)