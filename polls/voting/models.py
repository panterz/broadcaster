from django.db import models

# Create your models here.
class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date_published')

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)

class Area(models.Model):
    name = models.CharField(max_length=200)

class VoteManager(models.Manager):
    def get_yesno_votes(self):
        yes = Vote.objects.select_related().get(choice__choice_text='Yes')
        no = Vote.objects.select_related().get(choice__choice_text='No')
        return (len(yes), len(no))
        
class Vote(models.Model):
    choice = models.ForeignKey(Choice)
    area = models.ForeignKey(Area)
    