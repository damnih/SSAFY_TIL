from django.shortcuts import render, redirect
from .models import Reservation, models
from .forms import ReservationForm # 같은 폴더 내의 forms 안의 예약폼 ㅇㅇ

app_name = 'reservations'

# Create your views here.
def index(request):
    reservations = Reservation.objects.all()
    context = {
        'reservations': reservations
    }
    return render(request, 'reservations/index.html', context)


def new(request):
    # # forms에서 만든 모델폼을 html에 넘겨준대 그렇다면 렌더를 해야겠지 
    # # 모델폼을 넘겨준다는 건 context로 만들어서 넘겨준다는 뜻
    
    # # 근데 지금 create 함수 설명을 보니깐 new에 이 form을 받을 필요가 잇을까?? 
    # # 그니깐 얘는 html로 생성한 그 폼들을 전해주는 용도 거기에서 끝나는 거 같아

    # answer) 결국 모델폼이라는 거는 어떠한 틀이니깐 딱 정보를 담은 그 틀까지는 얘가 받아서 create에 넘겨줄거라는 거임
    # 이게 그 어제였나 그제 수업을 예로 들면 터미널에서 딱 save()누르기 전까지 
    # 막 article.title = "title" 이런식으로 담아줬잖아 
    # 이걸 form에서 입력받은 것 뿐이고, 
    # 같은 종류의 데이터셋들을 여기에 담아서 보관?? 해주고있다고 생각하면 될것같음 
    # 아직 생성까지의 단계는 아닌 거임 이거를 create에게 전달해야 비로소 생성이 되는 것임

    # # 그렇다면 받아온 모델폼을 또 담아줄(할당할) 변수가 필요하다는 뜻 
    form = ReservationForm(request.POST, request.FILES)
    
    # # # 여기에 유효성 검사 들어가줘야하는데,, 흠,,, 지금 당장 필요할까? 
    # # 역시 이거는 create에 써야 하는 거였어 

    # # # 일단 연습 겸 작성해보쟝 
    # # if is_valid(): # 유효하다면 
    # #     form # 그대로 전송
    # # # 근데 어떻게 전송하느냐? create의 과정과 동일하다 
    # #     # 아티클 생성하고 그걸 담아서 페이지에 보내고 끝  
    # #     # 완성된 페이지로 리다이렉트 
    # # # 유효하지 않다면
    # # # 기존 페이지를 오류명과 함께 다시 보이게 해서 유효한 폼을 보내도록 안내 
    
    # 즉 이렇게 담은 것들을 context 안에 담아서 렌더해주는거겟징 아니 근데 이 정보들을 new안에 담을 필요가,, 
    # 흠,, 아 html 작성하면서 action으로 create을 소환했잖아 거기에 쓴다고 생각하면 될 듯 

    context = {
        'form': form, 
    }

    return render(request, 'reservations/new.html', context)


def create(request):
    # 아니 이 모든 걸 하기 전에 먼저 해야하는게 있었어 
    # 요청이 POST로 들어온 경우에 한해서, 이것만이 옳은 요청이니깐 받아줄 거잖아 
    # 고로 이걸 먼저 조건문으로 걸러줘야겠지?
    if request.method == 'POST':
        # 그래서 포스트로 요청이 제대로 들어왔다면
        # 그렇다면 받아온 모델폼을 또 담아줄(할당할) 변수가 필요하다는 뜻 
        form = ReservationForm(request.POST, request.FILES)
        
        # 여기에 유효성 검사 들어가줘야함
        # 일단 연습 겸 작성해보쟝 
        if form.is_valid(): # 유효하다면 
            # 얘는 아티클 인스턴스가 되는 거임 ㅇㅇ 
            # 이 인스턴스를 다시 저장해주고 = 페이지 생성하고 
            form.save()
            # 이렇게 생성된 녀석은 pk가 있으니깐 
            return redirect('reservations:index')
            # form # 그대로 전송
        # 근데 어떻게 전송하느냐? create의 과정과 동일하다 
            # 아티클 생성하고 그걸 담아서 페이지에 보내고 끝  
            # 완성된 페이지로 리다이렉트 
        # 유효하지 않다면
        # 기존 페이지를 오류명과 함께 다시 보이게 해서 유효한 폼을 보내도록 안내 
    context = {
        'form': form, 
    }

    return render(request, 'reservations/new.html', context)