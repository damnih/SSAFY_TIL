from django.db import models


class Todo(models.Model):

    # 1) CharField + choices
    STATUS_CHOICES = [
        ('TODO', '할 일'),
        ('DOING', '진행 중'),
        ('DONE', '완료'),
    ]
    status = models.CharField(
        max_length=5,
        choices=STATUS_CHOICES,
        default='TODO',
        help_text='현재 작업 상태를 선택해주세요.',
        verbose_name='상태',
    )

    # 2) IntegerField + choices
    PRIORITY_CHOICES = [
        (1, '낮음'),
        (2, '보통'),
        (3, '높음'),
    ]
    priority = models.PositiveIntegerField(
        choices=PRIORITY_CHOICES,
        default=2,
        help_text='우선순위를 선택해주세요 (1=낮음, 2=보통, 3=높음).',
        verbose_name='우선순위',
    )

    # 기존 필드들
    title = models.CharField(max_length=100, verbose_name='제목')
    content = models.TextField(blank=True, verbose_name='내용')
    completed = models.BooleanField(default=False, verbose_name='완료 여부')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
