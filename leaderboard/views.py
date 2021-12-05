from django.shortcuts import render
from accounts.models import UserData


def ranking(request):
    rankList = list()
    abc = UserData.objects.all()
    for i in abc:
        rankList.append([i.num_ques_solved, str(i.user_id).title()])

    rankList = sorted(rankList, reverse=True)

    for i in range(len(rankList)):
        rankList[i].append(i + 1)

    return rankList


# Create your views here.
def home(request):
    ranks = ranking(request)
    return render(request, 'leaderboard.html', {'ranks': ranks})
