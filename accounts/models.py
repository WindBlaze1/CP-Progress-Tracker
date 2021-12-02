from django.db import models
from django.db.models.fields import CharField, IntegerField

# Create your models here.
class UserData(models.Model):
	user_id = IntegerField(primary_key=True)
	codechef_handle = CharField(max_length=50)
	codeforces_handle = CharField(max_length=50)
	atcoder_handle = CharField(max_length=50)
	num_ques = IntegerField(default=0)