from django.contrib import admin
# 명시적 상대경로
from .models import Article


# Register your models here.
# admin 사이트(site)에 등록(register) 한다.
admin.site.register(Article)
