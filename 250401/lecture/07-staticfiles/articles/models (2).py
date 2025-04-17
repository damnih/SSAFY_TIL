from django.db import models


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()

    # 이미지 스태틱?? 이거 미디어 
    # 이거 만드는건 어디에 써주든 상관은 없으나, 
    # 만들어지는 테이블의 모양새에는 차이가 없으나, 
    # 이 크리에이트앳과 업데이티드앳 두개는 자동으로 입력되는 거라 
    # 구분을 위해 교재에서는 이 사이에 써줬따고 함 
    image = models.ImageField(blank=True, upload_to='%Y/%m/%d/')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# 설계도 만드는 건 makemigrations 
# 그걸 디비에 적용하는건 migrate 

