from django.shortcuts import render
from .models import Author

# Create your views here.

def index(request):
    authors = Author.objects.all()
    context = {
        'authors': authors
    }
    return render(request, 'libraries/index.html', context)

def detail(request, aut_pk):
    # 여기서 담아줘야 하는 건 무엇일까? 
    # 그럼 여기서 pk값이 이거로는 불충분한거임 
    # 그렇다면 주소창에서 입력한 정수가 variable routing으로 들어와야하는데 어케? 
    # 아 인자로 받아주면 되는구나
    # 밖에서 온거니깐 인자로 받아주면 되는거였어 
    # 아 !!!! 
    author = Author.objects.get(pk=aut_pk)
    # authors = Author.objects.all()
    context = {
        'author': author
    }
    return render(request, 'libraries/detail.html', context)