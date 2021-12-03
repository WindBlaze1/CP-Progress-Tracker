from django.db import models
# from multiselectfield import MultiSelectField

# Create your models here.
class Event(models.Model):

	SITES = (
		('codechef.com', 'Codechef'),
		('codeforces.com', 'Codeforces'),
		('hackerearth.com', 'Hackerearth'),
		('leetcode.com', 'Leetcode'),
		('atcoder.jp', 'Atcoder'),
		('codingcompetitions.withgoogle.com', 'Google')
	)

	name : str
	time : str
	duration : str
	clink : str
	# host = MultiSelectField(choices = SITES)
	host : str
	calendar : str