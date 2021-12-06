from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_dynamic_ladder, name="get_dynamic_ladder"),
    path('<int:prob_id>/', views.get_problems, name="get_problems"),
]
