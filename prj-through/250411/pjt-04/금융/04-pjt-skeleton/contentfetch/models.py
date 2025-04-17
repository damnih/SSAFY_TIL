from django.db import models


class StockData(models.Model):
    company_name = models.CharField(max_length=255)
    stock_code = models.CharField(max_length=20)
    comments = models.TextField()  # 댓글을 텍스트로 저장
    analysis = models.TextField()  # ChatGPT 분석 결과
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name
