from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # 팔로잉 (내가 -> 누구를) (참조) 나를 중심으로 누군가를 찾는게 편하잖아 그걸 참조로 하는게 편함
    # 둘이 바뀌어도 로직상으론 상관 없는데 그래도 내가 생각하기 편한게 좋잖아  
    # 팔로워 (누가 -> 나를) (역참조)
    followings = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        # 나 자신 포함하는 재귀적인 관계가 될 거니깐 self 있구 대칭 꺼주고 
        related_name='followers',
        )
    # user.following.all() # 참조 
    # user.user_set.all() # 역참조 
    # 이건 둘다 사용자다보니깐 이렇게 생겨먹게 된거임
    # 그래서 relatedname을 이용해서 이름을 followers로 바꿔주는 거임
    # user.followers.all() # 이렇게 쓸 수 있음!!!! 


