from django.db import models
from django.conf import settings


# Create your models here.
class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    """
    M:N관계 설정 시 그냥 복수형으로 이름을 짓는 것 보다,
    지금 우리가 만드는 기능이 무엇인지 생각해보고 명시적인 매니저 이름을 설정하는 것이 좋다.
    
    게시글 1번에 좋아요를 누른 모든 유저 조회
    (Article -> User / 참조)

    `게시글1.users.all()` 표현을 다음과 같이 표현하는 것이 더 적합하다. 
    `게시글1.like_users.all()`
    """
    """
    [역참조 매니저 이름 충돌 상황]
    - Article : User (N:1)
        - article.user (참조)
        - user.article_set (역참조)
    - Article : User (N:M)
        - article.like_users (참조)
        - user.article_set  (역참조)
        - user.like_articles (새로운 역참조 이름으로 변경)
    - N:1 관계의 역참조 이름(_set)은 바꾸지 않는 것을 권장한다.
        - 개발 시 _set 이름만 봤을 때 "아 지금  N:1에서 역참조를 하는것이구나"를 명시적으로 알기 위함이다.
    """
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
    title = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
