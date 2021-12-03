from django.db import models
from django.db.models.fields import CharField, IntegerField
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey


# Create your models here.
class UserData(models.Model):
    user_id = ForeignKey(User, on_delete=models.CASCADE)
    codechef_handle = CharField(max_length=50)
    codeforces_handle = CharField(max_length=50)
    atcoder_handle = CharField(max_length=50)
    num_ques_solved = IntegerField(default=0)
    num_ques_att = IntegerField(default=0)
