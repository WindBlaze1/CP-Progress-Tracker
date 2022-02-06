from django.shortcuts import redirect, render
import requests as req
import os
from .models import Ladder
from django.contrib.auth.models import User
from django.contrib import messages


# To pre-render a ladder database
# for future use (if it does not exist)
def export_ladders():
    # Return this for use in dropdown menu
    for_dropdown = list()
    fs = os.listdir('saved')
    dirs = {}
    print('fs = ',fs)

    for f in fs:
        t = f.split('.')
        dirs[int(t[0])] = t[1].strip().replace('L', '<').replace('G', '>').replace(' ', '_') + '.' + t[2]

    dir2 = dirs
    dirs = {}
    for i in sorted(dir2):
        dirs[i] = dir2[i]

    for l_num in dirs:
        l_name = dirs[l_num].replace('_', ' ')
        for_dropdown.append([l_name[0:-4], l_num])

        # Name in saved folder
        fname = os.path.join('saved', str(l_num) + '. ' + dirs[l_num].replace('<', 'L').replace('>', 'G').replace('_', ' '))

        # If Ladder not found in DB
        if Ladder.objects.filter(name__startswith=l_name).count() == 0:
            # Make a new Ladder
            lad = Ladder(name=l_name)
            lad.save()

            # and fill the Ladder with contents of file(Problems)
            f = open(fname, 'r')
            total = 0

            for line in f.readlines():
                k = line.split('|')
                lad.problem_set.create(pid=k[1], name=k[0], link=str(k[3])[0:-1], difficulty=int(k[2]))
                lad.save()
                total += 1

            # Update total Questions
            lad.total_q = total
            lad.save()
        else:
            print('if condition false')

    return for_dropdown


def get_problems(request, prob_id=1):
    dropdown = export_ladders()

    handle = str()

    # Make a list of list to pass in render function
    print_ladder = list()
    ak = Ladder.objects.get(pk=prob_id).problem_set.all()
    solved = 0

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        handle = user.userdata_set.filter(user_id=user.id)[0].codeforces_handle
        if req.get('https://codeforces.com/api/user.status?handle=' + handle).json()['status'] == 'FAILED':
            msg = req.get('https://codeforces.com/api/user.status?handle=' + handle).json()['result']
            messages.error(request, msg)
            return redirect('/problems')
        else:
            obj = req.get('https://codeforces.com/api/user.status?handle=' + handle).json()

        all_problems_verdict = {}

        for submission in obj['result']:
            id = str(submission['problem']['contestId']) + submission['problem']['index']
            verdict = submission['verdict']

            if id not in all_problems_verdict:
                all_problems_verdict[id] = []

            if verdict not in all_problems_verdict[id]:
                all_problems_verdict[id].append(verdict)

        for k in ak:
            var = 0
            if k.pid in all_problems_verdict:
                if 'OK' in all_problems_verdict[k.pid]:
                    status = 'Accepted'
                    solved += 1
                    var = 1
                else:
                    status = all_problems_verdict[k.pid][0]
                    var = 2
            else:
                status = 'Not Attempted'
            print_ladder.append([k.name, k.link, status, k.difficulty, var])
    else:
        for k in ak:
            print_ladder.append([k.name, k.link, 'Not Attempted', k.difficulty])

    dropdown.sort(key=lambda x: x[1])

    return render(request, 'problems.html', {'ladder': print_ladder, 'items': dropdown, 'solved': solved, 'total': Ladder.objects.get(pk=prob_id).total_q})


def get_dynamic_ladder(request):
    
    ls = [1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200]

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        handle = user.userdata_set.filter(user_id=user.id)[0].codeforces_handle
        url = 'https://codeforces.com/api/user.info?handles=' + handle
        if req.get('https://codeforces.com/api/user.info?handles=' + handle).json()['status'] == 'FAILED':
            msg = req.get('https://codeforces.com/api/user.info?handles=' + handle).json()['result']
            messages.error(request, msg)
            return redirect('/problems')
        else:
            obj = req.get('https://codeforces.com/api/user.info?handles=' + handle).json()
        num = obj['result'][0]['rating']
        for i in range(10,0,-1):
            if num>ls[i]:
                return get_problems(request,i+1)

    return get_problems(request)