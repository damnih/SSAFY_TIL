from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views.decorators.http import require_POST
# Create your views here.

def index(request):
    posts = Post.objects.all()
    context = {
        # 문제 1 
        # 모든 출력이 되도록 수정, html 코드 보고 변수명을 맞춰줌 
        'posts': posts
    }
    return render(request, 'posts/index.html', context) 

def create(request):
    if request.method == 'POST':
        # 문제 8 
        # 이미지 등록 가능하게 만들기
        # form에 정보를 담을 때 이미지 파일을 따로 명시해줘야 함! 
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
# 숫자 인자 pk로 들어오는 거 맞음 
def update(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        # 포스트 요청이 맞자면 이 요청으로 들어온 내용을 폼에 담아줘야함
        form = PostForm(request.POST, instance=post, files=request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('posts:detail', pk=pk)
    else:
        form = PostForm(instance=post)
    context = {
        'post' : post,
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


# 문제 9
@require_POST 
def comment_delete(request, pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('posts:detail', pk=pk)  