from django.shortcuts import render
from userProfile.dash_apps.finished_apps import temp
from userProfile.dash_apps.finished_apps import temp10


# Create your views here.
def home(request):
    return render(request, 'profile.html')
