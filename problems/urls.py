from django.urls import path
from . import views

urlpatterns = [
    path('',views.get_problems,name="get_problems"),
    path('<int:prob_id>/',views.get_problems,name="get_problems"),
]