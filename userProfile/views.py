from django.shortcuts import render
from userProfile.dash_apps.finished_apps import temp10, temp9, temp8
from accounts.models import UserData
import requests as req


def codeforces_questions(username):
    problems_data = req.get('https://codeforces.com/api/user.status?handle=' + username).json()['result']
    problems_with_verdict = dict()

    for i in problems_data:
        if i['problem']['name'] in problems_with_verdict.keys() and i['verdict'] == 'OK':
            problems_with_verdict[str(i['problem']['contestId']) + i['problem']['index']] = 'OK'
        else:
            if str(i['problem']['contestId']) + i['problem']['index'] not in problems_with_verdict.keys():
                problems_with_verdict[str(i['problem']['contestId']) + i['problem']['index']] = dict()
                problems_with_verdict[str(i['problem']['contestId']) + i['problem']['index']] = i['verdict']
            else:
                problems_with_verdict[str(i['problem']['contestId']) + i['problem']['index']] = i['verdict']

    total_problems = len(problems_with_verdict)
    problems_solved = 0

    for i in problems_with_verdict:
        if problems_with_verdict[i] == 'OK':
            problems_solved += 1

    return problems_solved, total_problems


def user_info(request):
    abc = UserData.objects.get(user_id=request.user.id)
    solved, attempted = codeforces_questions(abc.codeforces_handle)
    abc.num_ques_att = attempted
    abc.num_ques_solved = solved
    abc.save()


def home(request):
    user_info(request)
    handles = {'cf_username': UserData.objects.get(user_id=request.user.id).codeforces_handle,
               'cc_username': UserData.objects.get(user_id=request.user.id).codechef_handle,
               'at_username': UserData.objects.get(user_id=request.user.id).atcoder_handle, }
    print(handles)

    return render(request, 'dashboard.html', handles)
