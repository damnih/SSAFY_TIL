from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    CATEGORY_CHOICES = [
        ('ELEC', 'Electronics'),
        ('BOOK', 'Books'),
        ('FASH', 'Fashion'),
    ]
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
    )

    # 다중 선택을 위해 기존 코드를 주석처리 후 다음 코드로 수정
    # 화면에 랜더링 되는 형태와, choices를 form에서 설정해줘야 함
    # category = models.CharField(
    #     max_length=500,
    #     help_text='콤마로 구분된 카테고리 코드',
    #     blank=True,
    #     verbose_name='카테고리',
    # )

    def __str__(self):
        return self.name

    def get_category_list(self):
        """콤마로 구분된 카테고리 문자열을 리스트로 변환"""
        if not self.category:
            return []
        return self.category.split(',')

    def get_category_display_list(self):
        """카테고리 코드에 해당하는 표시 이름 리스트 반환"""
        categories = self.get_category_list()
        category_dict = dict(
            [
                ('ELEC', 'Electronics'),
                ('BOOK', 'Books'),
                ('FASH', 'Fashion'),
            ]
        )
        return [category_dict.get(cat, cat) for cat in categories]

    def get_category_display(self):  # 원래 choices 필드에서 사용하는 메서드
        """카테고리 이름들을 콤마로 구분하여 반환"""
        return ', '.join(self.get_category_display_list())
