"""URL для about и rules."""
from django.urls import path

from . import views


app_name = 'pages'


urlpatterns = [
    path('about/', views.About.as_view(), name='about'),
    path('rules/', views.Rules.as_view(), name='rules'),
]

handler404 = 'pages.views.page_not_found'
