from django.db import models

class Ladder(models.Model):
    name = models.CharField(max_length=100)
    total_q = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.name + str(self.total_q)

    
class Problem(models.Model):
    pid = models.CharField(max_length=10,default='')
    name = models.CharField(max_length=100)
    difficulty = models.IntegerField()
    link = models.CharField(max_length=400)
    ladder = models.ForeignKey(Ladder,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
