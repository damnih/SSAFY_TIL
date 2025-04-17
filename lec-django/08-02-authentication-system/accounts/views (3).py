from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

# 나 여기 왜 임포트가 잘 안되는지 몰르겟네,,, 
# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# 원래 이랫던거 한번 삭제해봄 덮어써야 하니깐 
# 근데 그래도,, 안살아나네,, 왜지? ㅜ 

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        # form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # auth_login(request, 로그인 인증된 유저 객체)
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

@login_required 
def logout(request):
    auth_logout(request)
    return redirect('articles:index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save() # 폼 저장하구 
            return redirect('articles:index')
        
    else:
        # 회원가입 템플릿과 회원정보 작성을 위한 폼을 올림 
        # 그렇다면 폼 인스턴스가 필요~! 
        # form = 유저인포 
        # 아 그렇다면 이거 임포트가 필요하겠다 임포트하러 맨위로 가자! 
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }
    return render(request, 'accounts/signup.html', context)
    

@login_required
def delete(request):
    # 유저 객체를 삭제
    # 유저를 조회해야 할까? 
    # 회원탈퇴는 기본적으로 로그인된 상태에서 하는 거니깐~! 조회는 필요없당
    # 그렇다면 그 회원정보는 어디에 있을까?? 
    # 로그인된 상태의 그 세션에,, 있을거임 
    # 요청 객체 안에 어떤 사용자가 요청을 보내는 건지 이미 그 정보가 다 들어있음 
    # request.user 이게잇음 ㅇㅇ!! 
    # print(request.user)
    request.user.delete()
    return redirect("articles:index")


def update(request):
    if request.method == "POST":
        # 기존유저정보는 request.user에 들어잇음 
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("articles:index")
    else:
        # 이거 약간 클래스같은거라 생각하면 됨 
        # 폼이니깐 인스턴스 이렇게 생성해준 거라 생각하면 됨 그런 개념임 

        # 여기에 인스턴스를 채워줫어야 함 
        # 비밀번호 수정은말야 GET요청이란말이지?? 
        # GET요청이니깐 여기서 else를 타고 내려옴 form이 여기서 채워져서 
        # 전달되고 전달되어 change_password로 넘어가게 되는 거지 
        # 고로 여기 폼에 지금 로그인한 정보가 무엇인지 확인할 수 있게,, 
        # 인스턴스가 잘 채워져 있어야 함... 
        form = CustomUserChangeForm(instance=request.user) 
        # 비밀번호 수정이 불가능했던 이전의 코드는 아래와 같이 생겼었음 
        # form = CustomUserChangeForm() 
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


# path('<int:user_pk>/password/', views.change_password, name='change_password'),
# 여기에 variable_routing 있잖아 여기서 지정된 변수명을 
# 함수에서도 필수적으로 언급해줘야함 맞춰줘야함   
@login_required
def change_password(request, user_pk):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('articles:index')
        # pass
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form, 
    }
    return render(request, 'accounts/change_password.html', context)

