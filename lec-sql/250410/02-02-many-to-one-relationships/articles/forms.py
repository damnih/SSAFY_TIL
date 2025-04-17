from django import forms
from .models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'content',)
        # 여기서 fields 지정할 때 exclude를 써도 됨

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

