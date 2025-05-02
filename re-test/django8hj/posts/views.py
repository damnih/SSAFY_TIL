from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views.decorators.http import require_POST
# Create your views here.

def index(request):
    posts = Post.objects.all()
    context = {
        # index.html에서 참조할 이름을 정확히 작성해준다
        'posts': posts 
    }
    return render(request, 'posts/index.html', context) 

def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES) # 파일도 form에 담아줌
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

def update(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post, files=request.FILES) #  instance로 현재 수정할 post 추가, 이미지 첨부 수정도 가능하게 함
        if form.is_valid():
            form.save()
            return redirect('posts:detail', pk=pk)
    # GET 요청일때는 form 내용을 가진 채로 수정화면 렌더
    else:
        form = PostForm(instance=post)
    context = {
        'form' : form,
        'post' : post, # update.html에서 post.pk를 필요로 함. 
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