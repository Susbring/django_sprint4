"""Формы проекта"""
from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from blog.models import Post, Comment


User = get_user_model()


class CreateForm(forms.ModelForm):
    """Форма создания"""
    class Meta:
        model = Post
        exclude = ('author',)
        fields = '__all__'
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'})
        }


class CommentForm(forms.ModelForm):
    """Форма комментария"""
    class Meta:
        model = Comment
        fields = ('text',)


class ProfileForm(forms.ModelForm):
    """Форма профиля"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
