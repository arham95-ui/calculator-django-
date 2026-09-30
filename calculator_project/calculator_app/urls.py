# calculator_app/urls.py
from django.urls import path
from . import views

app_name = 'calculator_app'

urlpatterns = [
    path('', views.calculator_view, name='calculator'),
    path('history/', views.history_view, name='history'),
]