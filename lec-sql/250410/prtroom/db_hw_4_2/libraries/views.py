from django.shortcuts import render
from .models import Book, Review


# Create your views here.

def index(request):
    # 책 전체 목록을 확인할 수 있는 페이지 제공할거임 
    books = Book.objects.all()
    context = {
        'books': books,
    }
    return render(request, 'libraries/index.html', context)


def detail(request, book_pk):
    book = Book.objects.get(pk=book_pk)
    context = {
        'book': book,
    }
    return render(request, 'libraries/detail.html', context)
