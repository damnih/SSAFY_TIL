from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views.decorators.http import require_POST
# Create your views here.

def index(request):
    posts = Post.objects.all()
    context = {
        # 문제 1 
        # 변수명 수정 
        'posts': posts
    }
    return render(request, 'posts/index.html', context) 

def create(request):
    if request.method == 'POST':
        # 문제 8 
        # 이미지 등록 
        # files 인자에 넣어줄 것 선택해줌 
        form = PostForm(request.POST, files=request.FILES) 
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:index')
    else:
        form = PostForm()
    context = {
        'form': form
    }
    return render(request, 'posts/create.html', context)


def detail(request, pk):
    post = Post.objects.get(pk=pk)
    comment_form = CommentForm() 
    context = {
        'post': post,
        'comment_form': comment_form 
    }
    return render(request, 'posts/detail.html', context)


# 문제 6, 7
def update(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post, files=request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('posts:detail', pk=pk)
    # GET 요청일때는 form 내용을 가진 채로 수정화면 렌더
    # 즉 form 내용이 있어야하니깐 form을 찾아주고 
    # 그 form에 해당하는 내용은 기존에 존재하던 포스트에 존재하는 내용인거임 
    else: 
        # form = PostForm(request.POST) 
        form = PostForm(instance=post)
    context = {
        'post' : post, # update.html에서 post.pk를 필요로 함. 
        # 이래서 context로 post를 넘겨주는거구나 
        'form' : form,
    }
    return render(request, 'posts/update.html', context)        


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