"""Логика для доп. информации."""
from django.shortcuts import render
from django.views.generic import TemplateView


class About(TemplateView):
    """Страница с информацией о проекте."""

    template_name = 'pages/about.html'


class Rules(TemplateView):
    """Страница с правилами проекта"""

    template_name = 'pages/rules.html'


def page_not_found(reqest, exception):
    """Вью функция для кастомной 404"""
    return render(reqest, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """Вью функция для кастомной 403"""
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    """Вью функция для кастомной 500"""
    return render(request, 'pages/500.html', status=500)
