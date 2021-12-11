from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import UserData
from bs4 import BeautifulSoup
import requests as req


def codechef_check(username):
    r = req.get('https://www.codechef.com/users/' + username)
    soup = BeautifulSoup(r.text, 'html.parser')
    page_title = str(soup.find_all('title')[0])
    if username in page_title:
        return True
    else:
        return False


def atcoder_check(username):
    r = req.get('https://atcoder.jp/users/' + username)
    soup = BeautifulSoup(r.text, 'html.parser')
    page_title = str(soup.find_all('title')[0])
    if username in page_title:
        return True
    else:
        return False



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


# Create your views here.
def register(request):
	if request.method == 'POST':
		first_name = request.POST['full_name'].split(" ")[0]
		username = request.POST['user_name']
		email = request.POST['email']
		pass1 = request.POST['pass1']
		pass2 = request.POST['pass2']
		cf_handle = request.POST['cf_handle']
		cc_handle = request.POST['cc_handle']
		ac_handle = request.POST['ac_handle']

		if User.objects.filter(username=username).exists():
			messages.info(request, 'Username already exists')
			return redirect('register')

		if ' ' in username:
			messages.info(request, 'Username should not contain spaces')
			return redirect('register')

		if User.objects.filter(email=email).exists():
			messages.info(request, 'Email already used')
			return redirect('register')
		
		if pass1 != pass2:
			messages.info(request, 'Passwords are not matching')
			return redirect('register')

		req1 = req.get('https://codeforces.com/api/user.info?handles=' + cf_handle).json()

		if req1['status'] == 'FAILED':
			messages.info(request, req1['status'])
			return redirect('register')

		if len(cc_handle) and (not codechef_check(cc_handle)):
			messages.info(request, 'Wrong codechef username')
			return redirect('register')

		if (len(ac_handle)) and (not atcoder_check(ac_handle)):
			messages.info(request, 'Wrong atcoder username')
			return redirect('register')

		user = User.objects.create_user(
			username=username,
			first_name=first_name,
			email=email,
			password=pass1,
		)
		user.save()

		solved, attempted = codeforces_questions(cf_handle)

		user1 = user.userdata_set.create(
			codechef_handle=cc_handle,
			codeforces_handle=cf_handle,
			atcoder_handle=ac_handle,
			num_ques_att=attempted,
			num_ques_solved=solved,
		)
		user1.save()

		return redirect('login')

	else:
		system_messages = messages.get_messages(request)
		for message in system_messages:
			x = 0
		return render(request, 'signup.html')


def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)

		if user is not None:
			auth.login(request, user)
			return redirect('/profile')
	
		else:
			messages.error(request, 'Invalid Credentials')
			return redirect('/accounts/login')

	else:
		return render(request, 'login.html')


def signout(request):
	auth.logout(request)
	return redirect('/')
