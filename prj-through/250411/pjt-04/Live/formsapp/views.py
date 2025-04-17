from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import BaseForm, ContactForm, ExtendedForm, ProductForm, WidgetForm
from .models import Product


# Create your views here.
def form1(request):
    form = ContactForm()
    context = {
        'form': form,
    }
    return render(request, 'formsapp/form1.html', context)


def form2(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)  # 저장하지 않고 인스턴스 반환
            print(f'cleaned_data: {form.cleaned_data}')  # cleaned_data 확인
            print(
                f'cleaned_data 타입: {type(form.cleaned_data)}'
            )  # cleaned_data 타입 확인
            category_values = form.cleaned_data.get('category', [])
            category_string = ','.join(
                category_values
            )  # 카테고리 데이터를 콤마로 구분된 문자열로 변환
            product.category = category_string
            product.save()
            messages.success(
                request,
                f"제품 '{product.name}'이(가) 성공적으로 저장되었습니다!",
            )
            return redirect('formsapp:form2')
    else:
        form = ProductForm()

    # 저장된 제품 목록 가져오기
    products = Product.objects.all().order_by('-created_at')[:5]

    context = {
        'form': form,
        'products': products,
    }

    return render(request, 'formsapp/form2.html', context)


def form3(request):
    form = BaseForm()
    context = {
        'form': form,
    }
    return render(request, 'formsapp/form3.html', context)


def form4(request):
    form = ExtendedForm()
    context = {
        'form': form,
    }
    return render(request, 'formsapp/form4.html', context)


def form5(request):
    form = WidgetForm()
    context = {
        'form': form,
    }
    return render(request, 'formsapp/form5.html', context)
