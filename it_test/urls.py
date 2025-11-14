from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_questions, name='get_questions'),  # /questions/
    path('submit/', views.submit_test, name='submit_test'), # /questions/submit/
]
