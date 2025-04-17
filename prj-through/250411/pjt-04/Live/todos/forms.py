from django import forms

from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'content', 'status', 'priority']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '할 일을 입력하세요',
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': '상세 내용을 입력하세요',
                    'rows': 4,
                    'style': 'height: 120px !important; resize: none;',
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'priority': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
        }
        labels = {
            'title': '제목',
            'content': '내용',
            'status': '상태',
            'priority': '우선순위',
        }


class UpdateTodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'content', 'status', 'priority', 'completed']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '할 일을 입력하세요',
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': '상세 내용을 입력하세요',
                    'rows': 4,
                    'style': 'height: 120px !important; resize: none;',
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
            'priority': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),
        }
        labels = {
            'title': '제목',
            'content': '내용',
            'status': '상태',
            'priority': '우선순위',
        }
