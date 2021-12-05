from django.urls import path
from . import views
from userProfile.dash_apps.finished_apps import temp10, temp9, temp8

urlpatterns = [
    path('', views.home, name='userProfile'),
]
