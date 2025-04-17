from django.contrib.auth.decorators import login_required 
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_safe, require_POST


from .forms import ArticleForm, CommentForm
from .models import Article, Comment


# @require_safe 라는 거는 GET 메서드만 허용하는 데코레이터
# @require_POST 라는 거는 POST 메서드만 허용하는 데코레이터

# 여기 메인페이지에 모든 정보 주고 전시하기만 하는 곳이잖아? 포스트나 다른 메서드 안필요함 
# 다 거르면 됨 
@require_safe
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)

@require_safe
def detail(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm()
    # 특정 게시글에 작성된 모든 댓글 조회 (역참조)
    comments = article.comment_set.all()
    context = {
        'article': article,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'articles/detail.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            # 강사님 코드로는 지금 실행이 안돼서 AI에게 물어봐 수정해본 코드 
            article.user = request.user  # Assign the logged-in user
            article.save()  # Save the article with the user field set
            # 이거 동일하게 다 진행함 ㅇㅇ 언제 이걸 써넣었느냐? 
            # commit=False 채워넣기 전에 같이 시행함
            # NOT NULL 오류 메세지 보고 필요한게 
            # article.user라는 걸 알아서 그제서야 만들어준거 
            # 근데 게시글쓴사람 내가 따로 조회해야하나? 아니지 
            # 요청을 보낸 요청객체에 어떤 사람인지 다 들어잇음
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)


@login_required
@require_POST
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    # 만약 현재 로그인된 요청 유저와 글 작성자가 같다면, 그 때서야 지울 수 있음 
    if request.user == article.user:
        article.delete()
    return redirect('articles:index')


@login_required
@require_http_methods(['GET', 'POST'])
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


# 코멘트 생성이나 삭제는 GET요청도 아님 걍 pass 


# detail.html에 들어가면 애초에 method="POST"로 포스트 요청밖에 안받음 
@login_required
@require_POST
def comments_create(request, article_pk):
    # 어떤 게시글에 작성되는 댓글이 알려면 게시글을 먼저 조회
    article = Article.objects.get(pk=article_pk)
    # CommentForm을 활용한 댓글 생성
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        # 외래키 데이터를 넣으려면 댓글 인스턴스가 필요한데...
        # 댓글 인스턴스는 save() 호출이 완료되어야 반환됨
        # commit 키워드를 False로 바꾸면
        # 댓글 인스턴스는 생성해주지만 실제 DB에 아직 저장 요청은 보내지 않고 대기
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()
        return redirect('articles:detail', article.pk)
    context = {
        'comment_form': comment_form,
    }
    return render(request, 'articles/detail.html', context)


# 얘도 저 get이 GET요청이 아님 
# 얘는 디테일 페이지에서 모든 걸 수행하기 떄문에 POST이외의 통신은 ㄴㄴ하고잇음 

# 게시글 pk를 가져오는 두번째 방법 (url에서 넘겨주기)
@login_required
@require_POST
def comments_delete(request, article_pk, comment_pk):
    # 어떤 댓글이 삭제되는 것인지 조회
    comment = Comment.objects.get(pk=comment_pk)
    # 게시글 pk를 가져오는 첫번째 방법 (댓글 삭제 전에 게시글 번호 저장해두기)
    # article_id = comment.article.pk
    # 댓글 삭제
    
    # 근데 이 전에 이걸 요청하는 사람이 댓글 작성자와 같은지 확인을 해줘 
    # 본인의 댓글만 삭제할 수 있게 처리 
    if request.user == comment.user:
        comment.delete()
    # 첫번째 방법에 대한 return
    # return redirect('articles:detail', article_id)
    # 두번째 방법에 대한 return
    return redirect('articles:detail', article_pk)
