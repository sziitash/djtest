from django.db import models

# Create your models here.
class GoalNum(models.Model):
    id = models.IntegerField(blank=True, null=False,primary_key=True)
    name = models.CharField(max_length=50, blank=True)
    groupname = models.CharField(max_length=50, blank=True)
    goalnum = models.IntegerField(blank=True, null=True)
    playcount = models.IntegerField(blank=True, null=True)
    playtime = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'goal_num'

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)