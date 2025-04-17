from django.db import models

# Create your models here.
class Diary(models.Model):
    content = models.CharField(max_length=125)
    picture = models.ImageField(blank=True, upload_to='diary/%y/%b/%a')
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    # id = models.IntegerField(primary_key=) # 얘는 댓글 자체의 pk값 # 이건 자동생성됨 
    content = content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    diary = models.ForeignKey(Diary, on_delete=models.CASCADE) # 얘는 그 댓글이 달려있는 게시글의 pk값 