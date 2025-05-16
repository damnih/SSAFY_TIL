from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views.decorators.http import require_POST
# Create your views here.


# 문제 1
# 모든 조회한 항목들이 나오게 전체 조회해 context에 담아 렌더링 
def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'posts/index.html', context) 

def create(request):
    if request.method == 'POST':
        # form = PostForm(request.POST, instance=request.) 
        form = PostForm(request.POST) 
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            # image = Post.image
            # image = form.
            post.save()
            return redirect('posts:index')
    else:
        form = PostForm()
    context = {
        'form': form
    }
    return render(request, 'posts/create.html', context)

# 하... static 공부 좀 할 걸... 
# static 관련해서 문제가 왤케 많이 나와....... 




# 아니 객체 조회를 하는 것에서부터 문제가 생기면... 어케야 하는 걸까,,, 잘 생각해보자

# 일단 조회를 해야 해
# 나는 Post 모델에서 생성된 인스턴스를 조회할 거야 
# 단 하나의 그 걸 조회할 거야 
# get 맞는디...? 
# 그렇다면 Post모델에 pk가 제대로 생성이 안되어잇나?
# 아니 그건 자동으로 만들어지는 건데 뭔 소리야 ㅜㅜ 
# 일단 db확인하러 ㄱㄱ 
# 아....!!!!!!!!!!!!
# pk=1인 게시글이 애초에 존재하지 않아서 그런 거였음 
# 그렇다면,, 게시글 주소와 게시글 넘버가 균일하지 않은데??? 이건 어쩔 수 없나?? 
# 머 게시글의 pk 값과 게시글 0N이 꼭 일치해야만 한다고 조건을 걸은 건 아니니깐 어쩔 수 없을 듯...? 


def detail(request, pk):
    post = Post.objects.get(pk=pk)
    comment_form = CommentForm() 
    context = {
        'post': post,
        'comment_form': comment_form 
    }
    return render(request, 'posts/detail.html', context)



# 문제 6 수정 페이지 화면 출력 

# @require_POST 
# 아니 포스트 요청만 받을 수 있게 이렇게 데코레이터를 달면, 이 초반 수정 버튼을 누를 때 들어가는 요청이 GET이라 아예 진입이 불가능함
# 근데 이 views파일만 수정 가능하지 html은 수정하면 안되잖아..
# 그니깐 데코레이터를 쓸 수가 없어 !!!! 

def update(request, pk):
    # 먼저 수정할 글을 조회해 
    post = Post.objects.get(pk=pk)
    # 수정할 글을 받아준 뒤 그걸 글 주인과 로그인된 사람이 같아야지 수정 가능.. 근데 이거는 이 출력 문제랑 상관이 없어 ㅜㅜ 
    
    # 만약 이 요청이 포스트라면 
    if request.method == 'POST':
        # 수정하려고 받은 이 폼의 내용을 폼에 넣어줘 

        form = PostForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect('posts:detail', pk=pk)
    else: 
        form = PostForm()
    
    # context = {
    #     "post": post, 
    #     "form": form,
    # }

    return redirect('posts:detail', pk=pk)




def delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('posts:index')

def comment_create(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('posts:detail', pk=pk)
    else:
        form = CommentForm()
    context = {
        'comment_form': form,
        'post': post
    }
    return render(request, 'posts/detail.html', context)


@require_POST 
def comment_delete(request, pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('posts:detail', pk=pk)  
    # if request.user == comment.user:
        # comment.delete()
        # return redirect('posts:detail', pk=pk)  