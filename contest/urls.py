from django.urls import path
from . import views

urlpatterns = [
	path('', views.contest),
	path('form', views.form, name='form'),
]
