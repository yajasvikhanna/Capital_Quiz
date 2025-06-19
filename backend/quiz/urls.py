from django.urls import path
from . import views

urlpatterns = [
    path('question/', views.get_random_question, name='get_random_question'),
    path('check-answer/', views.check_answer, name='check_answer'),
    path('refresh-countries/', views.refresh_countries, name='refresh_countries'),
]