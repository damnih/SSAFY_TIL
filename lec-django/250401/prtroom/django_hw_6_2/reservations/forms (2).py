from django import forms 
from .models import Reservation

class ReservationForm(forms.ModelForm): # 그렇다면 여기서 적는 ModelForm은 기본 틀 이름 그자체인건가? 
    # 모델폼을 불러와서 쓰겠다는 그것 
    class Meta:
        model = Reservation # 그래서 여기서 어떠한 종류의 모델폼을 들고올 것인지 그 타입명을 설정해주고 
        fields = '__all__'



