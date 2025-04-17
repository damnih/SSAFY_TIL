from django import forms 
from .models import Article


# class ArticleForm(forms.Form):
#     title = forms.CharField(max_length=10)
#     content = forms.CharField(widget=forms.Textarea)

# 이 폼클래스는 사용자로부터 받는 인풋의 구조를 만들게 됨
# forms 라는 모듈 안에 있는 위젯 클래스임 


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

# meta class는 모델폼의 정보를 작성하는 곳임 
# 메타데이터 
# 클래스 배울 때 매직메서드다 뭐다 배운 적 있음 
# 더블 언더바 던더바 이런거 있었음 
# 튜플이나 리스트로도 만들 수 있기는 함 

