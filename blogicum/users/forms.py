"""Форма пользователя"""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Форма кастомного создания пользователя"""

    class Meta(UserCreationForm.Meta):
        model = User
