from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('email', )


# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=12)
#     password = forms.CharField(widget=forms.PasswordInput())

