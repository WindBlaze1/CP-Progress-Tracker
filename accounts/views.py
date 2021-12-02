from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import UserData

# Create your views here.
def register(request):

	if request.method == 'POST':
		first_name = request.POST['full_name'].split(" ")
		# first_name = request.POST['full_name'].split(" ")[0]
		# if len(name) >= 2:
		# 	last_name = request.POST['full_name'].split(" ")[1]

		username = request.POST['user_name']
		
		email = request.POST['email']
		pass1 = request.POST['pass1']
		pass2 = request.POST['pass2']
		cf_handle = request.POST['cf_handle']
		cc_handle = request.POST['cc_handle']
		ac_handle = request.POST['ac_handle']

		if User.objects.filter(username=username).exists():
			messages.info(request, 'Username already exists!!')
			return redirect('register')

		if ' ' in username:
			messages.info(request, 'Username should not contain spaces')
			return redirect('register')

		if User.objects.filter(email=email).exists():
			messages.info(request, 'Email already used!!')
			return redirect('register')
		
		if pass1 != pass2:
			messages.info(request, 'Passwords are not matching!!')
			return redirect('register')
		

		user = User.objects.create_user(
			username=username,
			first_name=first_name,
			email=email,
			password=pass1
		)
		user.save()

		user1 = UserData(
			user_id=user.id,
			codechef_handle=cf_handle,
			codeforces_handle=cc_handle,
			atcoder_handle=ac_handle,
		)
		user1.save()

		# messages.success(request, 'Account created!!')

		print('user created')
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
			print('authenticated!!')
			# should call the profile page
			return redirect('/profile')
			return render(request, "userProfile", {'username': user.username})
	
		else:
			messages.error(request,'invalid credentials')
			# messages.info(request,'invalid credentials')
			print('invalid credentials')
			return redirect('/')

	else:
		return render(request, 'login.html')

def signout(request):
	auth.logout(request)
	print('User Logged out!!')
	
	# under construction:
	return redirect('/')