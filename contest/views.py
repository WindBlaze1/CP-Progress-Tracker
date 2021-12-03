from django.http.response import HttpResponse
from django.shortcuts import render

from .models import Event
import requests
import datetime

list_of_events = []
selected_Hosts = []

list_of_sites = [
	'codechef.com',
	'codeforces.com',
	'hackerearth.com',
	'leetcode.com',
	'atcoder.jp',
	'google.com'
]

selected_HostsDict = {
	'codechef_com': False,
	'codeforces_com': False,
	'hackerearth_com': False,
	'leetcode_com': False,
	'atcoder_jp': False,
	'google_com': False
}

host_num = {
	0:'codechef_com',
	2:'codeforces_com',
	4:'hackerearth_com',
	8:'leetcode_com',
	16:'atcoder_jp',
	32:'google_com'
}

# to display the list_of_events in tabular form:
def displayContest(request, flagFilter,hosts):

	template = 'contests.html'
	# if (flagFilter):
	# 	template = 'filteredContests.html'

	return render(request, template, {
		'events': list_of_events, 
		'sites': selected_Hosts, 
		'list_of_sites': list_of_sites,
		'sitesCheck': selected_HostsDict,
		'list1':hosts
	})


# to convert seconds in days/hr/min
def durationConvert(sec):
	if (sec >= 86400):
		days = sec // 86400
		return (str(days) + " days")

	elif (sec >= 3600):
		hours = sec // 3600
		return (str(hours) + " hrs")

	else:
		minutes = sec // 60
		return (str(minutes) + " mins")


# main:
def contest(request,contest_id=0):
	try:
		response = requests.get('https://clist.by:443/api/v2/contest/?format=json&username=kartik_003&api_key=4ea81c7ab9aff64629287c2982b6ac14b0159e43&order_by=-start')
	except:
		return render(request, 'contests.html')


	url = response.json()
	# url = requests.get('https://clist.by:443/api/v2/contest/?format=json&username=kartik_003&api_key=4ea81c7ab9aff64629287c2982b6ac14b0159e43&order_by=-start').json()

	format = "%Y-%m-%d %H:%M:%S"
	
	for c_list in url['objects']:
		tempEvent = Event()

		tempEvent.host = c_list['host']
		tempEvent.name = c_list['event']

		# time:
		tempEvent.time = c_list['start'].split('T')[0] + " " + c_list['start'].split('T')[1]
		dateObj = datetime.datetime.strptime(tempEvent.time, format)
		dateObj += datetime.timedelta(hours=5, minutes=30)
		tempEvent.time = dateObj.strftime(format)

		tempEvent.duration = durationConvert(c_list['duration'])
		tempEvent.clink = c_list['href']
		list_of_events.append(tempEvent)

	# sort according to time
	list_of_events.sort(key = lambda x : x.time)
	
	contests = str(contest_id)
	while len(contests) < 6:
		contests = '0' + contests

	pass_val = []

	for k in (list_of_sites):
		if(k == '0'):
			pass_val.append('')
		else:
			pass_val.append('checked')

	return displayContest(request, False,pass_val)


def filter(request):

	# global selected_Hosts
	# selected_Hosts = []

	selected_Hosts.clear()

	for keys in selected_HostsDict:
		selected_HostsDict[keys] = False

	checkVar = 'checked'
	# checkVar = str(checkVar, 'utf-8')

	if request.method == 'GET':
		if (request.GET.get('codechef.com') == "True"):
			selected_Hosts.append("codechef.com")
			selected_HostsDict['codechef_com'] = True
			print("1: ", request.GET.get('codechef.com'))

		if (request.GET.get('codeforces.com', False)):
			selected_Hosts.append("codeforces.com")
			selected_HostsDict['codeforces_com'] = True
			print("2: ", request.GET.get('codeforces.com', False))

		if (request.GET.get('hackerearth.com', False)):
			selected_Hosts.append("hackerearth.com")
			selected_HostsDict['hackerearth_com'] = True
		
		# print("3: ", request.GET.get('hackerearth.com', False))

		if (request.GET.get('leetcode.com', False)):
			selected_Hosts.append("leetcode.com")
			selected_HostsDict['leetcode_com'] = True

		if (request.GET.get('atcoder.jp', False)):
			selected_Hosts.append("atcoder.jp")
			selected_HostsDict['atcoder_jp'] = True

		if (request.GET.get('google.com', False)):
			selected_Hosts.append("codingcompetitions.withgoogle.com/kickstart")
			selected_Hosts.append("codingcompetitions.withgoogle.com")
			selected_HostsDict['google_com'] = True


# def form(request):
# 	# filter(request)

# 	return displayContest(request, True)

# 	# return render(request, 'temp.html', {'sites': selected_Hosts})


def form(request):

	val = ''

	# if request.method == 'POST':
	
	for i in list_of_sites:
		if request.GET.get(i) == 'on':
			val = '1' + val
		else:
			val = '0' + val
	print(val)
	return contest(request,int(val))