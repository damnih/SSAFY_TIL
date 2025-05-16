from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import redirect, render

from articles.models import Article






from .forms import CustomUserChangeForm, CustomUserCreationForm


# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('articles:index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


def delete(request):
    request.user.delete()
    return redirect('articles:index')


def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


def change_password(request, user_pk):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)


def profile(request, username): 
    # username으로 어떤 유저인지ㅣ 조회
    # 근데 우리는 유저 클래스로 직접 참조하지 않는다는 장고와의 약속이 있었음
    # 그래서 유저를 조회하기 위해선 선택지가 두개 있었음
    # get_user_model() / settings.AUTH_USER_MODEL
    # 근데 저 후자는 models.py에서만 쓰기로 했었잖아
    # 고로 전자를 이용
    # 근데 얘는,, 임포트해서 써야 하는 함수지? 임포트하러 ㄱㄱ 
    # 사용자 인증 관련은 auth에서 임포트 ㄱㄱ 

    # get_user_model은 유저를 조회해주징 그래서 바로 객체 반환되니깐 일케 쓸 수 있음
    # get_user_model().objects.get(username=username)

    # 하지만 우리가 원래 알던 그 모양이 아니잖아... 어색하잖아..
    # 이렇게 걍 유저에 먼저 담아서 조회할 수 잇음 
    User = get_user_model()
    person = User.objects.get(username=username)
    context = {
        'person': person, 
    }
    return render(request, 'accounts/profile.html', context) 

def follow(request, user_pk): 
    # 상대방을 먼저 조회해야 함 내가! 팔로우할! 상대! 
    User = get_user_model()
    # 일단 유저 클래스가 필요하니깐 유저 객체 가져오고 
    you = User.objects.get(pk=user_pk)
    # 내가 이 사람을 팔할지 언팔할지 확인
    # 어케할거라고?
    # 기존에 팔되어있음 언팔, 언팔상태면 팔 
    # 즉 그건 저 사람!!! you의 팔로워 목록에 request.user 인 내가 있느냐 없느냐 
    # 근데 나를 좀 쉽게 판별하고 싶으니깐 변수에 일단 담아줄겡
    me = request.user

    # 자 그렇다면 조건문 시작
    # 하기 전에,, 
    # 팔로우 할 수 없는 경우가 잇음
    # 나 자신은 팔로우 못해,,
    # 그니깐 그것부터 먼저 확인을 해줘야해 
    # 팔로우 누르려는 내가, 팔로우하고싶은 너가 아니라면, 
    if me != you:
        # 만약 내가 너의 기존 팔로워였다면 
        if me in you.followers.all():
            # 다대다는 어느 방향에서 하든 다 먹히므로 1 or 2 아무거나 ㄱㄱ 
            # 1 니 팔로워에서 나 삭제
            you.followers.remove(me)
            # 2 내 팔로잉에서 너 삭제 
            # me.followings.remove(you)
        else:  
            # 1 니 팔로워에서 나 추가
            you.followers.add(me)
            # 2 내 팔로잉에서 너 추가가 
            # me.followings.add(you)
    return redirect('accounts:profile', you.username)


# 그렇다면 좋아요 기능 구현해보자~! 

def like(request, article_pk):
    # 내 정보는 요청에 들어가있으니깐, 인자로 보내줘야 하는 것은 게시글 번호~! 
    # 일단 내 정보 헷갈리니깐 me라는 변수에다가 넣어주자 !!! 구분을 위해서 !!!!!
    me = request.user
    # 얘 괄호가 필요한지 아닌지는 헷갈렸지만, 밑줄 안쳐지니깐 ㄱㅊ 

    # 이미 좋아요를 눌렀다면 취소, 안눌렀다면 좋아요 
    # 이거는 어케되냐? 이 게시글에 좋아요를 누른 사람들 리스트에서 나를 찾아주는거임 
    # 게시글과 좋아요를 누른 사람들은 다대다 리스트 안에 들어가있을거 아님? 
    # 다대다는 새로운 참조 테이블이 생성되는데, 이거 이름이 겹치니깐 일반적으론 models.py에서 related_name으로 이름 새롭게 지정해줌
    # 이거 확인해보고 소환해서 있는지 확인
    # class Article(models.Model):
    #     like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
    # 웅 articles/models.py 에서 확인해보니 이렇게 정해져 있었음~~!!!! 
    
    # pk로 호출한 특정 아티클 인스턴스에 대해 이게 있는지 없는지를 확인해주는 거니깐
    # 우선 pk로 특정 아티클을 소환!!! 
    article = Article.objects.get(pk=article_pk)
    # 이 특정 아티클의 좋아요 목록에 요청 객체(나)가 있다면? 
    if me in article.like_articles.all():
        # 좋아요 취소 
        # 저 리스트 안에서 내 정보를 삭제 
        article.like_articles.remove(me)

    # 아니라면
    else:
        # 좋아요 ok
        # 저 리스트에다가 내 정보를 추가 
        article.like_articles.add(me)
    
    return redirect('articles:index')

