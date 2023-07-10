from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import MyUser, Post, Comment
from django.contrib.auth import authenticate

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password1', 'password2']

class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': True})

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['picture', 'caption']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


